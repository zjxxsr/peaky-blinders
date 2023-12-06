import argparse

if '__main__' == __name__:
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--name', help='Name', type=str, default='default name')
    parser.add_argument('--batch', help='Batch size.', type=int, default=256)
    parser.add_argument('--lr', help='Learning rate.', type=float, default=None)
    parser.add_argument('--lr2', help='Learning rate 2.', type=float, default=0.001)

    args = parser.parse_args()

    xname = args.name
    xbatch = args.batch
    xlr = args.lr
    xlr2 = args.lr2

    print('name', xname)
    print('batch', xbatch)
    print('lr', xlr)
    print('lr2', xlr2)
