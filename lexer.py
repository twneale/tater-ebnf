from re import escape as e

from rexlex import Lexer, include, bygroups


class Lexer(Lexer):
    re_skip = r'\s+'
    dont_emit = [
        'String.Start', 'String.End',
        'Comment.Start', 'Comment.End',
        ]
    re_identifier = r'(?i)[a-z_][a-z_\d]*'

    tokendefs = {

        'root': [
            include('statement'),
            ],

        'statement': [
            ('Assignment.Identifier', re_identifier, 'statement.op'),
            ],

        'statement.op': [
            ('Op.Equals', e(r'::='), 'statement.body'),
            ('Op.Equals', e(r':='), 'statement.body'),
            ('Op.Equals', e(r'='), 'statement.body'),
            ],

        'statement.body': [
            include('expression'),
            ('Op.Semicolon', e(r';'), '#pop'),
            ],

        'expression': [
            include('values'),
            include('operators'),
            ],

        'values': [
            include('literals'),
            include('identifiers'),
            include('metachars'),
            ],

        'literals': [
            ('Literal.Number.Real', '\d+\.\d*'),
            ('Literal.Number.Int', '\d+'),
            ('Quote.Open', r'"', 'dq_string'),
            ('Quote.Open', r"'", 'sq_string'),
            ('Literal.String.Hex', '#x[A-Z0-9]+'),
            ],

        'identifiers': [
            ('Identifier', re_identifier),
            ],

        'metachars': [
            ('Option.Start', e('['), 'option'),
            ('Repeat.Start', e('{'), 'repeat'),
            ('Comment.Start', e('(*'), 'comment'),
            ('Group.Start',   e('('), 'group'),
            ],

        'operators': [
            ('Op.Concat', e(r',')),
            ('Op.Pipe', e(r'|')),
            ('Op.Hyphen', e(r'-')),
            ('Op.Star', e(r'*')),
            ('Op.Plus', e(r'+')),
            ('Op.Qmark', e('?')),
            ],

        # --------------------------------------------------------------------
        #
        # --------------------------------------------------------------------
        'option': [
            ('Literal.String', r'[^\]]+'),
            ('Literal.String', e('\]')),
            ('Option.End', e(']'), '#pop'),
            ],

        'repeat': [
            ('Literal.String', e('\}')),
            ('Repeat.End', e('}'), '#pop'),
            include('expression'),
            ],

        'group': [
            ('Literal.String', e('\)')),
            ('Group.End', e(')'), '#pop'),
            include('expression'),
            ],

        'comment': [
            (bygroups('Comment', 'Comment.End'), r'(?s)(.+?)(\*\))'),
            ],

        'dq_string': [
            ('Literal.String', r'\\"'),
            ('Literal.String', r'[^\\"]+'),
            include('unicode_string'),
            ('Quote.Close', r'"', '#pop'),
            ],

        'sq_string': [
            ('Literal.String', r"\\'"),
            ('Literal.String', r"[^\\']+"),
            include('unicode_string'),
            ('Quote.Close', r"'", '#pop'),
            ],

        'unicode_string': [
            ('Literal.String.Unichr', r'\\u\d+'),
            ('Literal.String', r'\\\\u(\d+)'),
            ('Literal.String', r'\\\\r\\\\n'),
            ],

        }

if __name__ == '__main__':
    with open('xmlebnf.txt') as f:
        grammars = [
    '''
    letter = "A" | "B" | "C" | "D" | "E" | "F" | "G"
           | "H" | "I" | "J" | "K" | "L" | "M" | "N"
           | "O" | "P" | "Q" | "R" | "S" | "T" | "U"
           | "V" | "W" | "X" | "Y" | "Z" ;
    digit = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;
    symbol = "[" | "]" | "{" | "}" | "(" | ")" | "<" | ">"
           | "'" | '"' | "=" | "|" | "." | "," | ";" ;
    character = letter | digit | symbol | "_" ;

    identifier = letter , { letter | digit | "_" } ;
    terminal = "'" , character , { character } , "'"
             | '"' , character , { character } , '"' ;

    lhs = identifier ;
    rhs = identifier
         | terminal
         | "[" , rhs , "]"
         | "{" , rhs , "}"
         | "(" , rhs , ")"
         | rhs , "|" , rhs
         | rhs , "," , rhs ;

    rule = lhs , "=" , rhs , ";" ;
    grammar = { rule } ;
    ''',

    '''
    syntax = (syntax_rule), {(syntax_rule)};
    syntax_rule = meta_identifier, '=', definitions_list, ';';
    definitions_list = single_definition, {'|', single_definition};
    single_definition = syntactic_term, {',', syntactic_term};
    syntactic_term = syntactic_factor,['-', syntactic_factor];
    syntactic_factor = [integer, '*'], syntactic_primary;
    syntactic_primary = optional_sequence | repeated_sequence |
      grouped_sequence | meta_identifier | terminal_string;
    optional_sequence = '[', definitions_list, ']';
    repeated_sequence = '{', definitions_list, '}';
    grouped_sequence = '(', definitions_list, ')';
    (*
    terminal_string = "'", character - "'", {character - "'"}, "'" |
      '"', character - '"', {character - '"'}, '"';
     meta_identifier = letter, {letter | digit};
    integer = digit, {digit};
    *)
    ''',

    f.read(),

    ]

    import pprint
    import rexlex
    for qq in grammars:
        tt = []
        toks = Lexer(qq)
        # toks = Lexer(qq, loglevel=rexlex.TRACE)
        try:
            for t in toks:
                print(t)
                tt.append(t)
        finally:
            pass
            pprint.pprint(tt)
        import pdb; pdb.set_trace()