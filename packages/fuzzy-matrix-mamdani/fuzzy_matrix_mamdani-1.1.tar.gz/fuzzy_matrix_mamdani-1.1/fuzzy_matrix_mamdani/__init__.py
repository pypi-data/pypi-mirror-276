import matplotlib.pyplot as plt
import numpy as np
import math

# линия
def curve(bottom, top, x):
    return (x-bottom)/(top-bottom)
    
# трапеция
def Trapeze(bottom_left, top_left, top_right, bottom_right):
    def own(x):
        if (top_left<=x<=top_right): 
            return 1
        if (bottom_left<=x<top_left):
            return curve(bottom_left, top_left, x)
        if (top_right<x<=bottom_right):
            return curve(bottom_right, top_right,x)
        return 0
    return own

# треугольник
def Triangle(bottom_left, peak, bottom_right):
    def own(x):
        if (x==peak):
            return 1
        if (bottom_left<=x<peak):
            return curve(bottom_left, peak, x)
        if (peak<x<=bottom_right):
            return curve(bottom_right, peak, x)
        return 0
    return own

# Гауссовская
# a – координата максимума функции принадлежности; b – коэффициент концентрации функции принадлежности
def Gauss(a,b):
    def own(x):
        if (b > 0):
            return math.exp(-(x-a)**2/(2*b**2))  
        return 0
    return own

# нечеткий вектор
class FuzzyVector():
    def __init__(self, positive):
        self.truth = positive
    
    def __str__(self):
        return f"truth: {round(self.truth, 2)}"

    def truth(self):
        return self.truth
    
    def inverse(self):
        return FuzzyVector(1-self.truth)

    def conjunction(self, other):
        positive = self.truth * other.truth
        return FuzzyVector(positive)

    def disjunction(self, other):
        positive = 1 - (1-self.truth) * (1-other.truth)
        return FuzzyVector(positive)

    def implication(self, other):
        return FuzzyVector(max(self.truth+other.truth-1, 0))
        
def conjunction(vectors):
    v = FuzzyVector(1)
    for vector in vectors:
        v = v.conjunction(vector)
    return v

def disjunction(vectors):
    v = FuzzyVector(0)
    for vector in vectors:
        v = v.disjunction(vector)
    return v

# лингвистическая переменная
class Feature():    
    def __init__(self, name, units, min, max, inout):
        self.name = name
        self.units = units
        self.min = min
        self.max = max
        self.predicates=[]
        # Входной или рассчётный признак.
        self.inout = inout
        #Текущее значение для входных признаков
        self.value=None

        #Чтобы не дублировать создание каждый раз при вычислениях.
        self.linspace = None
        # Список правил, которые говорят о данном рассчётном признаке
        # чтобы много раз его не строить при вычислениях.
        self.rules = []

# термы ЛП
class FuzzyPredicate():
    def __init__(self, feature: Feature, name, func=None, const=None):
        self.feature: Feature = feature
        self.name = name
        #Для центроидного метода дефаззификации
        self.func = func
        #Для упрощённого метода дефаззификации
        self.const = const

    def scalar(self,x=None):
        if x is None:
            if self.const is None:  
                raise ValueError(f"Const value for predicate {self.feature.name} '{self.name}' is not specified!") 
            else:
                return self.const

        if self.func is None:
            raise ValueError(f"Function for predicate {self.feature.name} '{self.name}' is not specified!")    

        return self.func(x)

    def vector(self,x=None):
        return FuzzyVector(self.scalar(x))
    
# правила 
class Rule():
    def __init__(self, input_pridicates, output_pridicate, weight):
        self.inputs = input_pridicates
        self.output = output_pridicate
        self.weight=weight
        self.truth = None

    def __str__(self):
        input_texts = [str(input.feature.name)+' "'+str(input.name)+'"' for input in self.inputs]
        text = "If "
        text += " and ".join(input_texts)
        text += ", then " + str(self.output.feature.name) + ' "' + str(self.output.name) +'". '
        text += "Truth: "+str(self.weight)
        return text
    
class Mamdani():
    # агрегирование подусловий
    def __aggregation__(fis):
        for rule in fis.rules:
            inputs = rule.inputs
            rule.truth=min([input.scalar(input.feature.value) for input in inputs])

    # Активизация подзаключений
    def __activation__(fis):
        for rule in fis.rules:
            rule.truth = rule.truth*rule.weight
            
    # Композиция и дефаззификация программно реализуются внутри одного цикла,
    # поэтому их надо писать внутри одной функции.
    def calculate(fis):
        Mamdani.__aggregation__(fis)
        Mamdani.__activation__(fis)

        # В общем виде, у алгоритма может быть несколько выходных переменных,
        # для каждого выходного признака.
        # Поэтому на выходе должен быть массив.
        result = []
        for feature_out in fis.features_out:

            rules = feature_out.rules
            if len(rules)==0:
                print(f"There is no rules for target feature: {feature_out.name}")
                result.append(np.nan)
                continue   

            numerator = 0
            denominator = 0
            # Метод дефазификации с помощью расчёта центра масс.
            if fis.defuzzification=="Centroid":
                # Формируем набор значений из области значений выходного признака для расчёта интеграла.
                xarr = feature_out.linspace              
                for x in xarr:
                    y = max([min(rule.output.scalar(x), rule.truth) for rule in rules])
                    numerator += x*y
                    denominator += y  
            # Упрощённый метод дефазификации 
            elif fis.defuzzification=="Simple":
                for rule in rules:
                    numerator += rule.output.scalar()*rule.truth
                    denominator += rule.truth 

            if denominator!=0:
                result.append(numerator/denominator)
            else:
                #Ни одно из правил не выполнилось.
                result.append(np.nan)

        return result

class Matrix():
    # агрегирование подусловий
    def __aggregation__(fis):
        for rule in fis.rules:
            inputs = rule.inputs
            rule.truth=conjunction([input.vector(input.feature.value) for input in inputs])

    # Активизация подзаключений
    def __activisation__(fis):
        for rule in fis.rules:
            rule.truth=rule.truth.implication(FuzzyVector(rule.weight))


    # Композиция и дефаззификация программно реализуются внутри одного цикла,
    # поэтому их надо писать внутри одной функции.
    def calculate(fis):
        Matrix.__aggregation__(fis)
        Matrix.__activisation__(fis)

        # В общем виде, у алгоритма может быть несколько выходных переменных, для каждого выходного признака.
        # Поэтому на выходе должен быть массив.
        result = []
        for feature_out in fis.features_out:

            rules = feature_out.rules
            if len(rules)==0:
                print(f"There is no rules for target feature: {feature_out.name}")
                result.append(np.nan)
                continue

            numerator = 0
            denominator = 0
            # Метод дефазификации с помощью расчёта центра масс.
            if fis.defuzzification=="Centroid":
                # Формируем набор значений из области значений выходного признака для расчёта интеграла.
                xarr = feature_out.linspace              
                for x in xarr:
                    y = (disjunction([rule.output.vector(x).conjunction(rule.truth) for rule in rules])).truth
                    numerator += x*y
                    denominator += y  
            # Упрощённый метод дефазификации 
            elif fis.defuzzification=="Simple":
                for rule in rules:
                    numerator += (rule.output.vector().conjunction(rule.truth)).truth
                    # rule.truth - степень реализации правила в виде вектора, 
                    # rule.truth.truth - истинностная координата вектора степени реализации правила.
                    denominator += rule.truth.truth 

            if denominator!=0:
                result.append(numerator/denominator)
            else:
                #Ни одно из правил не выполнилось.
                result.append(np.nan)

        return result

class FuzzyInferenceSystem():
    def __init__(self):
        self.features_in = []
        self.features_out = []
        self.rules = []
        self.algorithm= None #Mamdani or Matrix
        self.defuzzification= None #Centroid or Simple
        self.num = 100 

    def create_feature(self, name, units, min, max, inout):
        feature = Feature(name, units, min, max, inout)
        if inout:
            self.features_in.append(feature)
        else:
            feature.linspace = np.linspace(feature.min, feature.max, self.num)
            self.features_out.append(feature)
        return feature

    def create_predicate(self, feature: Feature, name, func=None, const=None):
        # Проверка, что признак принадлежит данной системе.
        if (feature in self.features_in or feature in self.features_out):
            predicate = FuzzyPredicate(feature, name, func, const)
            feature.predicates.append(predicate)
            return predicate
        else:
            raise Exception("The feature does not belong to this system.")

    def create_rule(self, input_predicates, output_predicate, weight):
        # Проверка, что предикаты принадлежат данной системе.
        for predicate in input_predicates:
            if not(predicate.feature in self.features_in):
                raise Exception("The pridicates does not belong to this system.")

        if not(output_predicate.feature in self.features_out):
            raise Exception("The pridicate does not belong to this system.")

        rule = Rule(input_predicates, output_predicate, weight)
        self.rules.append(rule)
        # Чтобы при вычислении значения признака сразу использовать только релевантные правила.
        output_predicate.feature.rules.append(rule)
        return rule

    def predict(self,*x):
        # Проверка соответствия переданных значений количеству входных признаков.
        if (len(x) != len(self.features_in)):
            raise Exception("Not matching the number of input parameters.")

        if self.defuzzification != 'Centroid' and self.defuzzification != 'Simple':
            raise Exception("Supported values for paramether 'defuzzification' are 'Centroid', 'Simple'.")

        # Проверка соответствия переданных значений областям значений входных признаков.
        n=0
        for feature in self.features_in:
            if (feature.min<=x[n]<=feature.max):
                feature.value=x[n]
                n+=1
            else:
                raise Exception(f"The value of the '{feature.name}' does not match the range.")
                
        if (self.algorithm=='Mamdani'):
            return Mamdani.calculate(self)
        elif (self.algorithm=='Matrix'):
            return Matrix.calculate(self)
        else:
            raise Exception("Supported values for paramether 'algorithm' are 'Mamdani', 'Matrix'.")

    # Графики принадлежности предикатов 
    def show_view(self):
        lp=self.features_in+self.features_out
        for feature in lp:
            x=np.linspace(feature.min, feature.max, self.num)
            fig, ax = plt.subplots(1, len(feature.predicates))
            n=0
            for predicate in feature.predicates:
                y=[]
                for xx in x:
                    y.append(predicate.func(xx))
                ax[n].set(xlabel=feature.units, ylabel = "Степень нечеткости")
                ax[n].set_title(feature.name+f" '{predicate.name}'")
                fig.set_figwidth(8)
                fig.set_figheight(3)
                ax[n].plot(x, y, clip_on = False)
                plt.tight_layout()
                n+=1
            plt.show()
