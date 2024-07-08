def fix_file(file_name):
    '''
    >>> fix_file('bad')
    '''
    with open(file_name, "r") as f:
        data = f.readlines()
    fix_data = []
    for line in data:
        fix_data.append(line[3:6]+line[0:3]+line[6:])
    print(''.join(fix_data))
    with open('new_rules.txt', 'w') as g:
        g.write(''.join(fix_data))
    return
def file_for_drag(problems,preference):
    my_lst = [problem[0] for problem in problems if problem[1] == preference]
    with open('ProblemstoSolve.txt', "w") as f:
        for item in my_lst:
            f.write(item)
class UCSD_Dragon:
    '''
    >>> d1 = UCSD_Dragon("Coco",20)
    >>> UCSD_Dragon.total_num_of_Dragons
    1

    >>> d1.set_color("red")
    >>> d1.color
    'red'

    >>> print(d1)
    Coco is red

    >>> d1.cost_per_week(10)
    150

    >>> d2 = UCSD_Dragon('Peanut', 25)
    >>> print(d2)

    >>> UCSD_Dragon.number_of_dragons()
    2

    >>> d1 < d2
    True
    '''
    total_num_of_Dragons = 0
    def __init__(self,name,cost_per_day):
        UCSD_Dragon.total_num_of_Dragons += 1
        self.name = name
        self.cost_per_day = cost_per_day
    def set_color(self, color):
        self.color = color
    def number_of_dragons():
        return UCSD_Dragon.total_num_of_Dragons
    def __str__(self):
        try:
            return self.name + ' ' +  'is' + ' ' + self.color
        except:
            raise AttributeError('No Such Attribute')
    def cost_per_week(self, cleaning_fee):
         return self.cost_per_day * 7 + cleaning_fee

    def __lt__(self, other_dragon):
        if self.cost_per_day < other_dragon.cost_per_day:
            return True
        return False

class Adult_Dragon:
    '''
    >>> c = Adult_Dragon('Elizabeth', 100)
    >>> d = Baby_Dragon("Coco")
    >>> t = Baby_Dragon
    >>> print(d.name, d.weight)
    >>> print(d.slogan)
    >>> print(d)
    >>> t.introduction()
    >>> c.introduction()

    '''
    slogan = 'I produce fire'
    def __init__(self,d_type,weight):
        self.type = d_type
        self.weight = weight
    def __str__(self):
        return self.type
    def introduction(self):
        return self
class Baby_Dragon(Adult_Dragon):
    slogan = 'I drink milk'
    def __init__(self,name):
        self.name = name
        Adult_Dragon.__init__(self, 'baby', 30)
    def introduction():
        print('Hi')
    def __repr__(self):
        return 'Cute Baby'
