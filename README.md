# CS171 PA2

Jiaxi Ye && Zheren Dong 

Launch process:

`$python3 process.py <pid=0|1|2>`

`$python3 network.py`

Input format:

- `print blockchain | clock | balance|set|pqueue`

- `transfer P<?> <amount>` 
    
  e.g. `transfer P2 5`

  Or alternatively by pid: `transfer 1 5` 





Message format:

`sender, receiver, clock, payload`

Payload format:

`type: 'request'`

`type: 'reply'`, 

`type: 'release', transaction: [S,R,amount]`, 

`type: 'test'`

Event format
`type, (foreign_clock,) (transaction,) (args,)`
