#!/bin/bash

kill $(cat .processor_pids)
rm .processor_pids