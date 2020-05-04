# CS171 PA2

Jiaxi Ye && Zheren Dong 

Sample message:  
3receiveP1P2LetsDance


Launch process:

`$python3 process.py <pid=1|2|3>`


Input format:

- `print blockchain|clock|balance|set|pqueue`

- `local <event>` 
    
  e.g. `local abcdef`

- `send P<pid> <event>` 

  e.g. `send P1 qwerty`


Message format:

`sender, receiver, clock, payload`

Payload format:

`type: 'request'`

`type: 'reply'`, 

`type: 'release', transaction: [S,R,amount]`, 

`type: 'test'`

Event format
`type, (foreign_clock,) (transaction,)`
