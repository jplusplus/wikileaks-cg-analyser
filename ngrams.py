# -*- coding: utf-8 -*-
import argparse

def ngrams(input='', n_min=0, n_max=5):
    input = input.split(' ')
    output = []
    end = n_max
    for n in range(n_min+1, end+n_min+1):
        for i in range(len(input)-n+1):
            output.append(input[i:i+n])
    return output

def main(tokens='', n_min=0, n_max=5):
    # Print out ngrams
    return ngrams( str(tokens), int(n_min), int(n_max) )

# Command-line execution of the module
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # Command arguments
    parser.add_argument('-m', '--min', help="Minimum gram to extract.", dest="n_min", default=0)
    parser.add_argument('-x', '--max', help="Maximum gram to extract.", dest="n_max", default=5)
    parser.add_argument('tokens', help="String to analyze.")
    # Parse arguments
    args = parser.parse_args()
    # Print out the main function
    print main( **vars(args) )
