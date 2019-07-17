#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse

from scrapycra import CraWeather, ScraPyCra

parser = argparse.ArgumentParser(
    description="Python web scraper for automated timesheet reporting."
)
parser.add_argument(
    '-hn',
    '--happiness',
    metavar='happiness',
    required=True,
    choices=[i for i in range(1, 5)],
    type=int,
    help="The CRA happiness."
)
parser.add_argument(
    '-mv',
    '--motivation',
    metavar='motivation',
    required=True,
    choices=[i for i in range(1, 5)],
    type=int,
    help="The CRA motivation."
)
parser.add_argument(
    '-hl',
    '--headless',
    dest='headless',
    action='store_true',
    help="Activate headless mode."
)

args = parser.parse_args()

happiness = args.happiness
motivation = args.motivation + 4  # Weird value from the business.
headless = args.headless

cra_weather = CraWeather(happiness=happiness, motivation=motivation)

scrapycra = ScraPyCra(cra_weather=cra_weather, headless=headless)
scrapycra.run()
