# -*- coding: utf-8 -*-

import asyncio
import logging
import time

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

class F(object):
    ''' World Model: this is data, concepts as features and relationships between them. '''
    pass

class X(object):
    ''' Actions: these are automation scripts for complex pre-programmed routines. '''
    pass

class Y(object):
    ''' Goals: loss functions to extract risk features. '''
    pass

class Utils(object):
    ''' Operating system level I/O, and data transformation tools. '''
    pass

class Stats(object):
    ''' Primitive predictive models and visualization tools. '''
    pass

class Process(object):
    def __init__(self):
        self.F = F()
        self.X = X()
        self.Y = Y()

    async def collect(self):
        ''' Mostly uses Utils, to collect data. '''
        while True:
            ''' ETL: Extract(data)-Transform(data)-Load(data). '''
            logging.info('collect')
            await asyncio.sleep(1)
            
    async def predict(self):
        ''' Mostly uses Stats, to extract features. '''
        while True:
            ''' EWA: Extract(features)-Weight(evaluate risk)-Act(parametrize actions). '''
            logging.info('predict')
            await asyncio.sleep(2)

async def main():
    agent = Process()
    
    collecting_task = asyncio.create_task(agent.collect())
    predicting_task = asyncio.create_task(agent.predict())

    await asyncio.gather(collecting_task, predicting_task)

if __name__ == '__main__':
    asyncio.run(main())
