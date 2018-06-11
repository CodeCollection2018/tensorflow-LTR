
import sys
import numpy as np

import utils
from model import LogisticRegression, RankNet


def get_train_valid_data(train_ratio=0.8):
    qids = np.loadtxt("../data/qids.txt")
    labels = np.loadtxt("../data/labels.txt")
    features = np.loadtxt("../data/features.txt")

    # sample
    qids_unique = np.unique(qids)
    N = len(qids_unique)
    idx = np.arange(N)
    np.random.shuffle(idx)
    train_num = int(N * train_ratio)
    train_qids = qids_unique[idx[:train_num]]
    valid_qids = qids_unique[idx[train_num:]]

    train_ind = utils._get_intersect_index(qids, train_qids)
    valid_ind = utils._get_intersect_index(qids, valid_qids)

    X_train = {
        "feature": features[train_ind],
        "label": labels[train_ind],
        "qid": qids[train_ind]
    }

    X_valid = {
        "feature": features[valid_ind],
        "label": labels[valid_ind],
        "qid": qids[valid_ind]
    }

    return X_train, X_valid


def train_lr():
    utils._makedirs("../logs")
    logger = utils._get_logger("../logs", "tf-%s.log" % utils._timestamp())

    params = {
        "offline_model_dir": "../weights/lr",
        "batch_size": 32,
        "epoch": 20,
        "feature_dim": 2,

        "optimizer_type": "nadam",
        "init_lr": 0.001,
        "beta1": 0.975,
        "beta2": 0.999,
        "decay_steps": 1000,
        "decay_rate": 0.9,
        "schedule_decay": 0.004,
        "random_seed": 2018,
        "eval_every_num_update": 100,

        "fc_type": "fc",
        "fc_dim": 32,
        "fc_dropout": 0.,
    }

    X_train, X_valid = get_train_valid_data(train_ratio=0.8)

    model = LogisticRegression("lr", params, logger)
    model.fit(X_train, validation_data=X_valid, shuffle=True)
    model.save_session()


def train_ranknet():
    utils._makedirs("../logs")
    logger = utils._get_logger("../logs", "tf-%s.log" % utils._timestamp())

    params = {
        "offline_model_dir": "../weights/ranknet",
        "batch_size": 32,
        "epoch": 20,
        "feature_dim": 2,
        "factorization": True,
        "sigma": 1.,

        "optimizer_type": "nadam",
        "init_lr": 0.001,
        "beta1": 0.975,
        "beta2": 0.999,
        "decay_steps": 1000,
        "decay_rate": 0.9,
        "schedule_decay": 0.004,
        "random_seed": 2018,
        "eval_every_num_update": 100,

        "fc_type": "fc",
        "fc_dim": 32,
        "fc_dropout": 0.,
    }

    X_train, X_valid = get_train_valid_data(train_ratio=0.8)

    model = RankNet("ranknet", params, logger)
    model.fit(X_train, validation_data=X_valid, shuffle=True)
    model.save_session()


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "lr":
            train_lr()
        elif sys.argv[1] == "ranknet":
            train_ranknet()
    else:
        train_lr()


if __name__ == "__main__":
    main()