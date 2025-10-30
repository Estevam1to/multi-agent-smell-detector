#!/usr/bin/env python3

"""
An OpenAI api key is required to use this script.
This uses and advanced GPT-3 model with AI vai Github Copilot to write this command-line interface. 
"""
import os
import openai
import click


def submit_question(text):
    """This submits a question to the OpenAI API"""
    openai.api_key = os.getenv("OPENAI_API_KEY")
    prompt = text

    result = openai.Completion.create(
        prompt=prompt,
        temperature=0,
        max_tokens=300,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        model="text-davinci-003",
    )["choices"][0]["text"].strip(" \n")
    return result


# write a main function that invokes submit_question functions and print the result
@click.command()
@click.argument("text")
def main(text):
    """This is the main function that you ask the OpenAI API a question to get an answer

    Example: ./questionAnswerCli "Who won the 2020 Summer Olympics?"

    """
    print(submit_question(text))


if __name__ == "__main__":
    main()
