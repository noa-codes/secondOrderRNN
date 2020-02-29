import os
import time
import torch


def create_unique_logdir(logdir, root_logdir="log/"):
    """
    Creates a unique log directory using the directory name and the time stamp
    Takes in a unqiue directory name and optionally a root directory path
    The root directory path is default to "log/" since all logs should be stored 
    under that directory

    Example:
        > create_unique_logdir("baseline_lstm")
        "log/baseline_lstm_Y2020_M2_D27_h16_m5"
    """
    if logdir == "":
        return logdir
    localtime = time.localtime(time.time())
    time_label = "Y{}_M{}_D{}_h{}_m{}".format(localtime.tm_year, localtime.tm_mon, \
        localtime.tm_mday, localtime.tm_hour, localtime.tm_min)
    unique_logdir = os.path.join(root_logdir, logdir + "_" + time_label)
    os.makedirs(unique_logdir, exist_ok=True)
    return unique_logdir


def save_checkpoint(logdir, model, optimizer, epoch, loss, lr, best=None, score=None):
    """
    Saves model checkpoint after each epoch

    best: An optional string used to specify which validation method this best
    checkpoint is for
    score: The best score for the given validation metric specified by parameter best
    """
    checkpoint_dir = os.path.join(logdir, "checkpoints")
    os.makedirs(checkpoint_dir, exist_ok=True)
    if best:
        checkpoint_path = "{}/best_{}_{}.pth".format(checkpoint_dir, best, score)
    else:
        checkpoint_path = "{}/lr{}_epoch{}.pth".format(checkpoint_dir, lr, epoch)

    torch.save({
            'epoch': epoch,
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
            'loss': loss,
            }, checkpoint_path)

    if not best:
        print("Saving checkpoint to lr{}_epoch{}".format(lr, epoch))


def load_checkpoint(model_checkpoint, model, optimizer, device):
    """
    Loads a pretrained checkpoint to continue training
    model_checkpoint: Path of the model_checkpoint that ends with .pth
    """
    checkpoint = torch.load(model_checkpoint, map_location=device)
    model.load_state_dict(checkpoint["model_state_dict"])
    optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
    model.to(device)
    return model