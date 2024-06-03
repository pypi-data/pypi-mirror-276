import argparse

class params:
    @staticmethod
    def parse_args():
        """
        Parse command-line arguments.
        """
        rad = 'this radius [float]'
        parser = argparse.ArgumentParser()
        parser.add_argument('-r', '--radii', dest='radii', action='store', type=float, required=True, help=rad)
        args = parser.parse_args()
        return args

    def calculate(self, radii, *args, **kwargs):
        """
        Calculate the volume of a sphere given its radius.
        """
        vol = (4/3) * (22/7) * radii**3
        return vol

    @staticmethod
    def test_args(args):
        """
        Test the validity of the parsed arguments.
        """
        assert args.radii >= 0, f'The radius is a negative number ({args.radii})'

if __name__ == '__main__':
    # Parse command-line arguments
    args = params.parse_args()
    
    # Validate arguments
    params.test_args(args)
    
    # Instantiate the class and perform the calculation
    #foo = Fooetalparam()
    result = params().calculate(args.radii)
    
    # Print the result
    print(f'Result: {result}')