#!/usr/bin/env python
"""Sample script of recurrent neural network language model.

This code is ported from following implementation written in Torch.
https://github.com/tomsercu/lstm

"""
from __future__ import print_function
import argparse
import math
import sys
import time

import numpy as np
import six
import json
from sklearn.cross_validation import train_test_split

import six.moves.cPickle as pickle

import chainer
from chainer import cuda
import chainer.links as L
from chainer import optimizers
from chainer import serializers

import net

parser = argparse.ArgumentParser()
parser.add_argument('--initmodel', '-m', default='',
                    help='Initialize the model from given file')
parser.add_argument('--resume', '-r', default='',
                    help='Resume the optimization from snapshot')
parser.add_argument('--gpu', '-g', default=-1, type=int,
                    help='GPU ID (negative value indicates CPU)')
parser.add_argument('--epoch', '-e', default=39, type=int,
                    help='number of epochs to learn')
parser.add_argument('--unit', '-u', default=650, type=int,
                    help='number of units')
parser.add_argument('--batchsize', '-b', type=int, default=20,
                    help='learning minibatch size')
parser.add_argument('--bproplen', '-l', type=int, default=35,
                    help='length of truncated BPTT')
parser.add_argument('--gradclip', '-c', type=int, default=5,
                    help='gradient norm threshold to clip')
parser.add_argument('--test', dest='test', action='store_true')
parser.set_defaults(test=False)

args = parser.parse_args()
xp = cuda.cupy if args.gpu >= 0 else np

n_epoch = args.epoch   # number of epochs
n_units = args.unit  # number of units per layer
batchsize = args.batchsize   # minibatch size
bprop_len = args.bproplen   # length of truncated BPTT
grad_clip = args.gradclip    # gradient norm threshold to clip

# Prepare dataset (preliminary download dataset by ./download.py)
vocab = {}
def parse_words(lyrics):
    words = "".join(lyrics).replace("Chorus:", "").replace(" \n\n", "<eos> ").replace("\n\n", "<eos> ").replace(' \n', '<eos> ').replace('\n', '<eos> ').replace("<eos><eos>", '<eos>').strip().split()
    dataset = np.ndarray((len(words),), dtype=np.int32)
    for i, word in enumerate(words):
        if word not in vocab:
            vocab[word] = len(vocab)
        dataset[i] = vocab[word]
    return dataset

lyrics = json.load(open("country_lyrics.json"))
use, valid_songs = train_test_split(lyrics,test_size=0.1)
train_songs, test_songs = train_test_split(use,test_size=0.2)
train_data = parse_words(train_songs)
valid_data = parse_words(valid_songs)
test_data = parse_words(test_songs)

print('#vocab =', len(vocab))
with open('vocab.bin', 'wb') as f:
    pickle.dump(vocab, f)

# Prepare RNNLM model, defined in net.py
lm = net.RNNLM(len(vocab), n_units)
model = L.Classifier(lm)
model.compute_accuracy = False  # we only want the perplexity
for param in model.params():
    data = param.data
    data[:] = np.random.uniform(-0.1, 0.1, data.shape)
if args.gpu >= 0:
    cuda.get_device(args.gpu).use()
    model.to_gpu()

# Setup optimizer
optimizer = optimizers.SGD(lr=1.)
optimizer.setup(model)
optimizer.add_hook(chainer.optimizer.GradientClipping(grad_clip))

# Init/Resume
if args.initmodel:
    print('Load model from', args.initmodel)
    serializers.load_npz(args.initmodel, model)
if args.resume:
    print('Load optimizer state from', args.resume)
    serializers.load_npz(args.resume, optimizer)


def evaluate(dataset):
    # Evaluation routine
    evaluator = model.copy()  # to use different state
    evaluator.predictor.reset_state()  # initialize state
    evaluator.predictor.train = False  # dropout does nothing

    sum_log_perp = 0
    for i in six.moves.range(dataset.size - 1):
        x = chainer.Variable(xp.asarray(dataset[i:i + 1]), volatile='on')
        t = chainer.Variable(xp.asarray(dataset[i + 1:i + 2]), volatile='on')
        loss = evaluator(x, t)
        sum_log_perp += loss.data
    return math.exp(float(sum_log_perp) / (dataset.size - 1))


# Learning loop
whole_len = train_data.shape[0]
jump = whole_len // batchsize
cur_log_perp = xp.zeros(())
epoch = 0
start_at = time.time()
cur_at = start_at
accum_loss = 0
batch_idxs = list(range(batchsize))
print('going to train {} iterations'.format(jump * n_epoch))

for i in six.moves.range(jump * n_epoch):
    x = chainer.Variable(xp.asarray(
        [train_data[(jump * j + i) % whole_len] for j in batch_idxs]))
    t = chainer.Variable(xp.asarray(
        [train_data[(jump * j + i + 1) % whole_len] for j in batch_idxs]))
    loss_i = model(x, t)
    accum_loss += loss_i
    cur_log_perp += loss_i.data

    if (i + 1) % bprop_len == 0:  # Run truncated BPTT
        model.zerograds()
        accum_loss.backward()
        accum_loss.unchain_backward()  # truncate
        accum_loss = 0
        optimizer.update()
    if (i + 1) % 100 == 0:
        # Evaluate on test dataset
        print('test')
        test_perp = evaluate(test_data)
        print('test perplexity:', test_perp)
        # Save the model and the optimizer
        print('save the model')
        serializers.save_npz('rnnlm.model', model)
        print('save the optimizer')
        serializers.save_npz('rnnlm.state', optimizer)
    if (i + 1) % 10000 == 0:
        now = time.time()
        throuput = 10000. / (now - cur_at)
        perp = math.exp(float(cur_log_perp) / 10000)
        print('iter {} training perplexity: {:.2f} ({:.2f} iters/sec)'.format(
            i + 1, perp, throuput))
        cur_at = now
        cur_log_perp.fill(0)

    if (i + 1) % jump == 0:
        epoch += 1
        print('evaluate')
        now = time.time()
        perp = evaluate(valid_data)
        print('epoch {} validation perplexity: {:.2f}'.format(epoch, perp))
        cur_at += time.time() - now  # skip time of evaluation

        if epoch >= 6:
            optimizer.lr /= 1.2
            print('learning rate =', optimizer.lr)

    sys.stdout.flush()

# Evaluate on test dataset
print('test')
test_perp = evaluate(test_data)
print('test perplexity:', test_perp)

# Save the model and the optimizer
print('save the model')
serializers.save_npz('rnnlm.model', model)
print('save the optimizer')
serializers.save_npz('rnnlm.state', optimizer)
