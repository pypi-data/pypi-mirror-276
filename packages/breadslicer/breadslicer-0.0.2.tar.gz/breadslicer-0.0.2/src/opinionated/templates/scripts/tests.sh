#!/bin/sh

pytest --cov --cov-report term --cov-report xml:coverage.xml --junitxml report.xml .