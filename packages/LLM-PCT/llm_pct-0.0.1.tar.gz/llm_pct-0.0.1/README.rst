Political Compass Test (PCT)
============================

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://opensource.org/licenses/MIT

- GitHub: `https://github.com/isabellahoch/LLM_PCT`_
- Free software: MIT license

Overview
--------

The Political Compass Test (PCT) is a Python package that allows users to proctor the political compass test algorithmically by allowing LLMs to react to PCT questions with open-ended responses. It classifies responses in agreement levels according to a specified threshold, then directly interacts with the `PCT website <https://www.politicalcompass.org/test>`_ to determine the generator's political position on the compass.

Features
--------

- Elicits responses to questions for the political compass test
- Classifies generated responses to determine their political position
- Programmatically interacts with PCT website to take the test and determine results
- Displays PCT results on interactive plot

Setup
-----

Expects a file path to a ``pct-assets`` directory with ``crx/adblock.crx`` extension and subdirectories for generated ``response``, ``score``, ``results`` files.

.. _`https://github.com/isabellahoch/LLM_PCT`: https://github.com/isabellahoch/LLM_PCT