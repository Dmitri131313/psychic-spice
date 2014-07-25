import human
import random

PUBERTY_AGE = 16

class ASocium( object ):
    def __init__( self ):
        object.__init__( self )
        self.__women        = []
        self.__young_men    = []
        self.__adult_men    = []

    def AddHuman( self, new_human ):
        """
        Adds new human to the socium.
        """
        if new_human.GetGender() == human.MALE:
            if new_human.IsSexuallyActive():
                self.__adult_men.append( new_human )
            else:
                self.__young_men.append( new_human )
        else:
            self.__women.append( new_human )

    def GetTotalPopulation( self ):
        return len( self.__women ) + len( self.__young_men ) + len( self.__adult_men )

    def GetTotalMalePopulation( self ):
        return len( self.__young_men ) + len( self.__adult_men )

    def GetAdultMalePopulation( self ):
        return len( self.__adult_men )

    def GetYoungMalePopulation( self ):
        return len( self.__young_men )

    def GetFemalePopulation( self ):
        return len( self.__women )

    def GetCustomMageStatusPopulation( self, mage_status ):
        mage_statuses = ( human.MAGE, human.HALF_MAGE, human.NOT_MAGE )
        assert mage_status in mage_statuses
        res = 0
        for man in self.__young_men:
            if man.GetMageStatus() == mage_status:
                res += 1
        for man in self.__adult_men:
            if man.GetMageStatus() == mage_status:
                res += 1
        for woman in self.__women:
            if woman.GetMageStatus() == mage_status:
                res += 1
        return res 

    def __Reproduce( self ):
        for woman in self.__women:
            mother_years = woman.GetSexAges()
            if len( mother_years ) == 0:
                continue
            new_children = mother_years.count( woman.GetActualAge() )
            if new_children > 0 and self.GetAdultMalePopulation() > 0:
                father = random.choice( self.__adult_men )
                children = [ woman.GiveBirth( father ) for i in range( new_children ) ]
                for child in children:
                    self.AddHuman( child )

    def __GrowUp( self ):
        for man in self.__adult_men:
            man.IncreaseAge()
        for woman in self.__women:
            woman.IncreaseAge()
        for boy in self.__young_men:
            boy.IncreaseAge()
            if boy.GetActualAge() >= PUBERTY_AGE:
                self.__adult_men.append( boy )
            self.__young_men = [ boy for boy in self.__young_men if boy.GetActualAge() < PUBERTY_AGE ]

    def __ExcludeDead( self ):
        self.__women        = [ woman for woman in self.__women if woman.IsAlive() ]
        self.__adult_men    = [ man for man in self.__adult_men if man.IsAlive() ]
        self.__young_men    = [ man for man in self.__young_men if man.IsAlive() ]

    def LiveOneYear( self ):
        self.__Reproduce()
        self.__GrowUp()
        self.__ExcludeDead()

    def GetAverageAge( self ):
        age_sum = 0
        for woman in self.__women:
            age_sum += woman.GetActualAge()
        for man in self.__young_men:
            age_sum += man.GetActualAge()
        for man in self.__adult_men:
            age_sum += man.GetActualAge()

        if age_sum == 0:
            return age_sum
        else:
            return round( float( age_sum ) / self.GetTotalPopulation(), 2 )
