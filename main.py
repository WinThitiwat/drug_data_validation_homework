import argparse
import sys
import metadata_analysis as meta
import mic_analysis as mic

analysis_dispatcher = {
    '1_1': meta.question1_1,
    '1_2': meta.question1_2,
    '1_3': meta.question1_3,
    '1_4': meta.question1_4,
    '1_5': meta.question1_5,
    '2_1': mic.question2_1,
    '2_2': mic.question2_2,
    '2_3': mic.question2_3,
    '2_4': mic.question2_4,
    '2_5': mic.question2_5,
}

def get_arguments():
    parser = argparse.ArgumentParser(description='Metadata and MIC analysis')

    parser.add_argument('-t', '--topic', default='1', metavar='Topic', required=True, dest='topic', help='Choose topic between 1 (Metadata), 2 (MIC). Default set to 1')
    parser.add_argument('-n', '--number', default='1', metavar='Question Number', required=True, dest='number', help='Choose question number between 1 - 5. Default set to 1')

    args = parser.parse_args()
    return args

def validate_input_argument(argument):
    topic = argument.topic
    number = argument.number

    try:
        if not topic.isnumeric() or not number.isnumeric():
            raise TypeError('Expect an integer input value')

        if int(topic) < 1 or int(topic) > 2:
            raise ValueError('Invalid Topic input.  Make sure to enter between 1 and 2')

        if int(number) < 1 or int(number) > 5:
            raise ValueError('Invalid Question Number input. Make sure to enter from 1 to 5')

    except Exception as exp:
        print('Error: Invalid input found')
        print(exp)
        sys.exit(1)

def main():

    # get input arguments
    argument = get_arguments()

    # validate input 
    validate_input_argument(argument)
        
    # assign variable accordingly
    topic = argument.topic
    question_number = argument.number

    # run analysis according to the input arguments
    topic_number = f'{topic}_{question_number}'
    analysis_dispatcher[topic_number]()

if __name__ == '__main__':
    main()