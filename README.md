### Logistics CLI

To Run: 
1. Install requiremnts `pip install -r requirements.txt`
2. All necessary data for `app/` is in the `data` directory
3. Navigate to the `app/` directory
4. From the CLI, run `python cli.py --help` for a list of commands

#### Commands
`flight-legs`
* Given a three-letter airport code, calculate the total inbound and outbound seats for that airport
* Options include: `--airport`/ `-a`, `--structure` / `-s` 
* `--structure` flag is used for the output format
  * `df` - DataFrame 
  * `dict` -> Dict 
  * `matrix` -> Matrix 
    * Data returned for Matrix is returned as `(Row Index, Column Index) Total Seats` where Row Index is the specified airport and Column Index represents the detination airport
* If not specifying an aiport, you can use `--num` to change the number of output rows for the `df` option only


`airport-from-index`
* Given an integer value, find the corresponding airport code
* Intended as a utility to lookup the airport corresponding to the column index of the related flight data
* Options include: `--idx` / `-i`
* Example:
  * `python cli.py airport-from-index -i 0` -> `LHR`
