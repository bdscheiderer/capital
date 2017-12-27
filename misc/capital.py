# file here for reference - can be run from python 3 console
# State Capital Quiz

import random

capitals = {'Alabama': 'Montgomery', 'Alaska': 'Juneau',
            "Arizona": 'Phoenix', 'Arkansas': 'Little Rock',
            'California': 'Sacramento', 'Colorado': 'Denver',
            'Connecticut': 'Hartford', 'Delaware': 'Dover',
            'Florida': 'Tallahassee', 'Georgia': 'Atlanta',
            'Hawaii': 'Honolulu', 'Idaho': 'Boise',
            'Illinois': 'Springfield', 'Indiana': 'Indianapolis',
            'Iowa': 'Des Moines', 'Kansas': 'Topeka',
            'Kentucky': 'Frankfort', 'Louisiana': 'Baton Rouge',
            'Maine': 'Augusta', 'Maryland': 'Annapolis',
            'Massachusetts': 'Boston', 'Michigan': 'Lansing',
            'Minnesota': 'Saint Paul', 'Mississippi': 'Jackson',
            'Missouri': 'Jefferson City', 'Montana': 'Helena',
            'Nebraska': 'Lincoln', 'Nevada': 'Carson City',
            'New Hampshire': 'Concord', 'New Jersey': 'Trenton',
            'New Mexico': 'Santa Fe', 'New York': 'Albany',
            'North Carolina': 'Raleigh', 'North Dakota': 'Bismarck',
            'Ohio': 'Columbus', 'Oklahoma': 'Oklahoma City',
            'Oregon': 'Salem', 'Pennsylvania': 'Harrisburg',
            'Rhode Island': 'Providence', 'South Carolina': 'Columbia',
            'South Dakota': 'Pierre', 'Tennessee': 'Nashville',
            'Texas': 'Austin', 'Utah': 'Salt Lake City',
            'Vermont': 'Montpelier', 'Virginia': 'Richmond',
            'Washington': 'Olympia', 'West Virginia': 'Charleston',
            'Wisconsin': 'Madison', 'Wyoming': 'Cheyenne'}

def clear():
    print(' \n' * 5)

def intro():
    print('')
    print('Welcome to the state capital quiz game!')
    print('')
    print("Please choose either the 20 question quiz, or try the full 50 question \n quiz to test your knowledge of all the state capitals!")
    print('')
    choice = ''
    while choice not in ('a', 'A', 'b', 'B'):
        choice = input("Choose 'A' for the 20 question quiz, or 'B' for the full 50 question quiz: ")
    print('')
    return(choice.upper())

def quiz(capitals, num):
    total_correct = 0
    allstates = list(capitals.keys())
    cities = []
    i = 1
    list4 = ('1','2','3','4')
    if num < 50:
        states = random.sample(allstates, num)
    else:
        states = allstates
    for state in states:
        allcities = list(capitals.values())
        # identify correct answer
        capital = capitals[state]
        # get three more possible answers and random shuffle answers
        allcities.remove(capital)
        cities = random.sample(allcities, 3)
        cities.append(capital)
        random.shuffle(cities)
        # ask quiz questions
        print('')
        print(str(i)+'. What is the capital of '+state+'?')
        print('')
        print('1.  ', cities[0])
        print('2.  ', cities[1])
        print('3.  ', cities[2])
        print('4.  ', cities[3])
        print('')
        guess = 0
        while guess not in list4:
            guess = input('Choose answer 1, 2, 3 or 4: ')
        print('')
        if cities[int(guess)-1] == capital:
            print('Correct! '+capital+' is the capital of '+state+'.')
            total_correct += 1
        else:
            print('Sorry that is not correct! '+capital+' is the capital of '+state+'.')
        print('')
        i += 1
    print('')
    print('You answered '+str(total_correct)+' out of '+str(num)+' correctly.')
    grade = round(total_correct/num, 2) * 100
    if total_correct == num:
        print('PERFECT score, congratulations!')
    elif grade >= 90:
        print('Excellent!')
    else:
        print('Good job, keep practicing!')

def main():
    new_game = 'Y'
    while new_game[0].upper() not in ("N"):
        clear()
        choice = intro()
        if choice == 'A':
            num = 20
        else:
            num = 50
        quiz(capitals, num)
        print('')
        new_game = input("Play again (Y/N)? ")

    else:
        print('')
        print('Thank you for playing the state capital quiz game!')
        print('')

main()

# end
