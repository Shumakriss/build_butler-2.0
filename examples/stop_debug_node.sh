#!/bin/bash

kill $(cat .debug_pids)
rm .debug_pids