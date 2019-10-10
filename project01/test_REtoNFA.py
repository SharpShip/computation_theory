
from regular_expression import RE
from nfa import NFA, State
from nfa import generate_state

EMPTY_STRING = ''

def generate_head_nfa(alphabet):
    """ generate a head nfa(->[s0])

    generate a nfa that only has an initial state,
    which is also the the start state and this nfa doesn't have final state

    Args:
        aplhabet : alphabet of the constucting nfa
    Returns:
        nfa : A NFA object that only has an initial state,
              which is also the the start state and this nfa doesn't have final state
    Raises:
    """
    s0 = generate_state()
    nfa = NFA(alphabet, [s0], s0, [])
    return nfa

def generate_aciton_nfa(action, alphabet):
    """ generate the nfa that recognizes the action string

    Args:
        aplhabet : alphabet of the constucting nfa
    Returns:
        nfa : A NFA object recognizes the action string
    Raises:
    """
    nfa = generate_head_nfa(alphabet)

    # add a new state object and add it to the final_states object
    f_state = generate_state()
    nfa.add_f_state(f_state)

    # add a function item that takes action string from start_state to f_state
    nfa.add_function_item(nfa.get_start_state(),
                          action,
                          f_state)
    return nfa

def read_or(s, alphabet, nfa1):
    """ deal with the or situation

    in read_or function,
    we separate the string into two substrings in the position of '|',
    and regard two part as two independent nfas,
    use or operator to combine these two nfas

    Args:
        aplhabet : alphabet of the constucting nfa
        nfa1 : the nfa that recoginize the previous
               regular expresssion string
    Returns:
        if nfa is None(haven't recogized string before): return action_nfa
        if not : return nfa + action_nfa
    Raises:
    """
    nfa2 = _trans_RE_to_NFA(s, alphabet)
    return nfa1 | nfa2

def read_repeat(s, alphabet, nfa):
    # TODO(ShipXu): This fuction reserved for XiaoHanHou.
    # Your code here
    pass

def read_parentheses(s, nfa):
    # TODO(ShipXu): This fuction reserved for XiaoHanHou.
    # Your code here
    pass

def read_add(action, alphabet, nfa=None):
    """ deal with the add situation

    generate nfa that recogize the action string
    if nfa is None(haven't recogized string before): return action_nfa
    if not : return nfa + action_nfa

    Args:
        alphabet : alphabet of the constucting nfa
        nfa : the nfa that recoginize the previous
              regular expresssion string
    Returns:
        if nfa is None(haven't recogized string before): return action_nfa
        if not : return nfa + action_nfa
    Raises:
    """
    action_nfa = generate_aciton_nfa(action, alphabet)
    if nfa is None:
        return action_nfa
    else:
        return nfa + action_nfa

def read_token(s, alphabet, nfa=None):
    """recursively deal with the regular expresssion string

    we can classsify the questions as four type:
    * : read_repeat,
    | : read_or,
    ( : read_parentheses
    other : read_add and some other operation
    if nfa is None(haven't recogized string before), we use nfa
    to store the content we recognize in the recursive process.

    Args:
        alphabet : alphabet of the constucting nfa
        nfa : the nfa that recoginize the previous
            regular expresssion string
    Returns:
    Raises:
    """
    if not s:
        return nfa

    if s[0] == '*':
        return read_repeat(s[1:], alphabet, nfa)
    elif s[0] == '|':
        return read_or(s[1:], alphabet, nfa)
    elif s[0] == '(':
        return read_parentheses(s[1:], nfa)
    else:
        return read_token(s[1:], alphabet, read_add(s[0], alphabet, nfa))

def _trans_RE_to_NFA(s, alphabet):
    """ transform the string of Regular Expression to be a nfa

    Args:
        s: the string of regular expression
        alphabet : alphabet of the constucting nfa
    Returns: nfa that equals to s
    Raises:
    """
    return read_token(s, alphabet)

def trans_RE_to_NFA(re):
    """ transform Regular Expression obeject to be a nfa

    Args:
        re : A Regular Expression object.
    Returns: nfa that equals to re
    Raises:
    """
    return _trans_RE_to_NFA(re.s, re.alphabet)

if __name__ == '__main__':
    # alphabet = ['a', 'b']

    regualar_string = 'a|b|c'
    alphabet = list(set([word for word in regualar_string
                         if word.isalpha() or word.isdigit()]))
    re = RE(alphabet, regualar_string)
    # re = RE(alphabet, 'a*')
    nfa = trans_RE_to_NFA(re)
    print(nfa)