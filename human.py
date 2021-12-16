import random

X_CHROMOSOME = "X"
Y_CHROMOSOME = "Y"

MAG_CHROMOSOME = "M"
NMAG_CHROMOSOME = "N"

MALE = "MALE"
FEMALE = "FEMALE"

MAGE = "MAGE"
HALF_MAGE = "HALF_MAGE"
NOT_MAGE = "NOT_MAGE"
SUPER_MAGE = "SUPER_MAGE"

MIN_SEX_AGE = 13
MAX_SEX_AGE = 60

CHANCE_TO_BE_MAGE = 0.1
CHANCE_TO_BE_SUPER_MAGE = 10 ** (-6)


def LoadedToss(probability):
    toss = random.random()
    return toss < probability


class AHuman:
    """
    A class that represents our "magic" human beings. Each human have only two kinds of genes.
    Sexual genes (or, maybe, chromosomes; biologists should correct me) determines human's gender.
    "Magic" genes determines will this human be a mage, a half-mage or an ordinary human.

    Each of that humans grows up to its max age and reproduces.
    """

    _magi_born = 0

    def __init__(self, sex_genes=(X_CHROMOSOME, X_CHROMOSOME), mag_genes=(NMAG_CHROMOSOME, MAG_CHROMOSOME)):
        """
        Constructor of AHuman object, which takes as its parametres sex and magic genes.
        Other parametres will be randomly defined depending on these two tuples.
        By default our human is half-mage woman.
        """
        object.__init__(self)

        self.__sex_genes = sex_genes
        self.__mag_genes = mag_genes
        self.__age = 0
        self.__children = 0
        self.__alive = True

        self.__DefineGender()
        self.__DefineMageStatus()
        self.__DefineMaxAge()

    def __str__(self):
        return f"Human: [{self.__gender}, {self.__mage_status}, {self.__age}/{self.__max_age}]"

    def __DefineGender(self):
        """
        Defines human's gender depending on its sex_genes. XX is female, XY is male.
        """
        if self.__sex_genes[0] == self.__sex_genes[1]:
            self.__gender = FEMALE
        else:
            self.__gender = MALE

    def __DefineMageStatus(self):
        """
        Defines human's magic powers on its mag_genes.
        NN is not mage, NM is half-mage, MM is mage.
        """
        # if self.__mag_genes[0] == self.__mag_genes[1] == MAG_CHROMOSOME:
        #     self.__mage_status = MAGE
        # elif self.__mag_genes[0] == self.__mag_genes[1] == NMAG_CHROMOSOME:
        #     self.__mage_status = NOT_MAGE
        # else:
        #     self.__mage_status = HALF_MAGE
        mage = LoadedToss(CHANCE_TO_BE_MAGE)
        super_mage = LoadedToss(CHANCE_TO_BE_SUPER_MAGE)
        if mage:
            self.__mage_status = MAGE
            AHuman._magi_born += 1
            if super_mage:
                self.__mage_status = SUPER_MAGE
        else:
            self.__mage_status = NOT_MAGE

    def __DefineMaxAge(self):
        """
        Defines how long human will live using gaussian distribution.
        """
        if self.__mage_status == NOT_MAGE:
            mean, deviation = 60, 4
        elif self.__mage_status == HALF_MAGE:
            mean, deviation = 103, 6
        elif self.__mage_status == MAGE:
            mean, deviation = 30, 5
        elif self.__mage_status == SUPER_MAGE:
            mean, deviation = 250, 50
        else:
            mean, deviation = 157, 10

        age = random.gauss(mean, deviation)
        age = int(round(age))
        self.__max_age = age

    def GetSexGene(self):
        """
        Returns sex_gene as a tuple.
        """
        return random.choice(self.__sex_genes)

    def GetMageGene(self):
        """
        Returns mag_genes as a tuple.
        """
        return random.choice(self.__mag_genes)

    def GetGender(self):
        """
        Returns human's gender.
        """
        return self.__gender

    def GetMageStatus(self):
        """
        Returns human's mage status (mage, half-mage, not mage).
        """
        return self.__mage_status

    def GiveBirth(self, father):
        """
        If human is female it gives birth t
        """
        # new_sex_gene = (self.GetSexGene(), father.GetSexGene())
        self.__children += 1
        father.__children += 1
        female = LoadedToss(0.5)
        if female:
            return AHuman._MakeFemale()
        else:
            return AHuman._MakeMale()
        # new_mag_gene = (self.GetMageGene(), father.GetMageGene())
        # child = AHuman(new_sex_gene, None)
        # return child

    def __Die(self):
        """
        Just kills our human.
        """
        assert self.__alive
        self.__alive = False

    def IncreaseAge(self):
        """
        Increases human's age year by year until it dies.
        """
        self.__age += 1
        if self.__age >= self.__max_age:
            self.__Die()

    def GetActualAge(self):
        """
        Returns human's actual age.
        """
        return self.__age

    def GetMaxAge(self):
        """
        Returns human's max age.
        """
        return self.__max_age

    def IsAlive(self):
        """
        Tells us, is human alive or not.
        """
        return self.__alive

    def IsSexuallyActive(self):
        """
        Tells us is human male ready for making babies or not.
        """
        # assert self.__gender == MALE
        return self.__age >= 16

    def IsReadyToGiveBirth(self):
        if self.__mage_status in (MAGE, SUPER_MAGE):
            return False
        if 20 <= self.__age <= 24:
            return LoadedToss(0.5)
        else:
            return False

    @staticmethod
    def _MakeFemale():
        return AHuman()

    @staticmethod
    def _MakeMale():
        return AHuman(sex_genes=(X_CHROMOSOME, Y_CHROMOSOME))

    @staticmethod
    def GetTotalMagiBorn():
        return AHuman._magi_born

    @staticmethod
    def DropMagiBorn():
        AHuman._magi_born = 0
