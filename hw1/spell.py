outFile = open('./spell.fst', 'w')

oneDict = {}
seqDict = {}
complexDict = {}
probDict = {}

stateCounter = 0

pho-a -> A
pho-b -> B or V
pho-ch -> C H
pho-d -> D
pho-e -> E
pho-f -> F
pho-g -> G
pho-h -> J
pho-i -> I
pho-k (when followed by pho-e or pho-i) -> Q U
pho-k (when followed by pho-s) -> X
pho-k (when followed by pho-a, pho-l, pho-o, pho-r, or pho-u) -> C
pho-l -> L
pho-m -> M
pho-n -> N
pho-o -> O
pho-p -> P
pho-r -> R
pho-rr -> R R
pho-s (when preceded by pho-k) -> nothing
pho-s (when not preceded by pho-k) -> S
pho-t -> T
pho-th (when followed by pho-a, pho-o, or pho-u) -> Z
pho-th (when followed by pho-e or pho-i) -> C or Z
pho-u -> U
pho-y -> Y or L L
nothing -> H (NOTE: letter h is silent in Spanish.)

oneDict['pho-a'] = 'A'
oneDict['pho-d'] = 'D'
oneDict['pho-e'] = 'E'
oneDict['pho-f'] = 'F'
oneDict['pho-g'] = 'G'
oneDict['pho-h'] = 'J'
oneDict['pho-i'] = 'I'
oneDict['pho-l'] = 'L'
oneDict['pho-m'] = 'M'
oneDict['pho-n'] = 'N'
oneDict['pho-o'] = 'O'
oneDict['pho-p'] = 'P'
oneDict['pho-r'] = 'R'
oneDict['pho-s'] = 'S'
oneDict['pho-t'] = 'T'
oneDict['pho-u'] = 'U'
oneDict['*e*'] = 'H'

seqDict['pho-ch'] = ['C','H']
seqDict['pho-rr'] = ['R','R']

complexDict['pho-k'] = 
