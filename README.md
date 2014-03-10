# tornado-reading-notes

a reading note about tornado source code~

## serveral key points

- stack_context  
  As for me, it is so difficult to understand why tornado use stack_context.
  Here is some hints i found some where:
  - the author of motor lib talked about [it][1] in the tornado mailing list.
  - ref the [tornado documents][2].

  I still need some time to consume this concept.May i should read the motor code?

- gen.coroutine  
  In tornado world, not eveything is running in a socket.So how can we play aysnc in everywhere?Well,the answer is we can't at all.

  But tornado use some tricks,the [concurrent][3] lib in python.Especially,tornado use thread to handle blocking operations.And use the concept of 'futures' to handle job state.

  So, in a word,tornado use epoll to handle sockets read/write,but use threading and future to handle blocking op.And combine those two kind of things into a great event loop which you can think as a for loop in a big array.

- ioloop

- safety

## ref
- www.nowamagic.net/academy/detail/13321018
- TODO zhkzyth.com/.....

[1]: https://groups.google.com/forum/#!topic/python-tornado/S12qMWXt9h0
[2]: http://www.tornadoweb.org/en/branch2.3/stack_context.html
[3]: http://docs.python.org/3/library/concurrency.html
