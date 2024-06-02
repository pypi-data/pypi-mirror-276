token-distance is a versatile library designed for fuzzy token searching within texts. It can be used as a standalone
command line tool or integrated into other software as a library. This tool is particularly useful for applications in
data mining, natural language processing, and information retrieval where matching based on exact tokens is
insufficient.

The process begins by tokenizing the input texts, typically using whitespace, though regular expressions and custom
functions can also be employed. Following tokenization, each token from the search query is assigned a weight that
reflects its importance, which could depend on factors like token length or predefined criteria.

For each search token, token-distance identifies the most similar token in the target text based on these weights. The
core of the library's functionality lies in how it calculates similarity: it pairs each search token with the best
matching token in the target text and computes a weighted average of these pairings to produce a final similarity score.

The operations of token-distance are summarized in the chart below, which illustrates the step-by-step process from
tokenization to the calculation of similarity scores. 


![](source/_static/schema.png)


## Installation

Installation of token-distance is straightforward using pip, the Python package installer. This method ensures that the
library and its dependencies are correctly configured. Ensure you have Python and pip installed on your system before
proceeding.

````shell
pip install token-distance
````


## Usage

token-distance is flexible, functioning both as a command-line tool and as a library for integration into your software.

### Console

To compare two text files for token similarity, use the following command:


````shell
    token_distance_compare <path_to_token_file> <path_to_search_target_file>
````

For more complex tokenization, such as splitting text by commas or exclamation marks, you can use regular expressions:

````shell
    token_distance_compare <path_to_token_file> <path_to_search_target_file> \
    --tokenize-by "[\s,\.]" --regex 1
````

This command will tokenize the input texts at spaces, commas, and periods, enhancing the flexibility of the search.

### As Library

token-distance can also be configured programmatically to suit specific needs, such as integrating custom similarity
algorithms. Here's how you can set up a token distance calculation function using a configuration object:

````python
from collections.abc import Callable
from token_distance import from_config, Config

calculate_distance: Callable[[str, str], float] = from_config(Config(mean='geometric'))
````

This configuration uses a geometric mean to compute the similarity score between tokens, which is useful for certain
types of textual analysis.

token-distance can also obtain information about the actual matching of the tokens, if those are of interest:

````python
from collections.abc import Callable, Collection
from token_distance import match_from_config, MatchConfig, RecordingToken

get_best_matches: Callable[[str, str], Collection[RecordingToken]] = match_from_config(MatchConfig())
````


