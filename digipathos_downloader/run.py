import setup_checks
import download
import sys


if __name__ == "__main__":

    # Get command line args
    if len(sys.argv) >= 2:
        name_filter = str(sys.argv[1])
    else:
        name_filter = "all"

    # Run main function
    download.main(name_filter, True)
