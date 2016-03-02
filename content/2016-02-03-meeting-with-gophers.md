---
layout: post
title: "Meeting with gophers"
modified: 2016-02-03 16:29:16 +0000
category: []
tags: [go, golang, programming]
image:
  feature: http://i.imgur.com/QhQdQY5.png
  credit: 
  creditlink: 
comments: True
share: 
---

I've decided that it's time to get to grips with a new programming language for
2016. After some thinking (trust me, I didn't over think this) I opted for [Go](http://golang.org).
There were a few choices to pick from:

* [io](http://iolanguage.org/)
* [Pharo](http://pharo.org/) (Smalltalk)
* [Rust](https://www.rust-lang.org/)

I've tried Go before and had a [brief](http://unlogic.co.uk/2015/01/12/solving-project-euler-with-rust-1/)
[fling](http://unlogic.co.uk/2015/01/20/solving-project-euler-with-rust-2/) with Rust. I had a
*very* quick dabble with io too. Technically when I did some work in Objective-C I kinda 
wrote smalltalkish code too. But I wanted to go a little deeper, and spend some decent 
time with one of these.

Short story shorter: I selected Go

Some of you might be asking "Why the fuck did you not choose Rust?". Well, it's
gaining traction and it's certainly talked about amongst my friends. But I was never really
taken by it. Then I watched [this video](https://www.youtube.com/watch?v=f6kdp27TYZs) and
the whole idea of *goroutines* and *channels* really appealed to me. I know Rust has channels too, but
the Go implementation sits better with me.

"But Sven", I hear you say, "what about the stop-the-world garbage collector?". Ah yes, the ol STWGC.
I am well aware that some high interactivity web services have been written in C++ after
the GC put a spanner in the works, but having read the release notes for 
[Go 1.5's GC](https://golang.org/doc/go1.5#gc) sound very promising, and lets face it,
I can live with a little bit of a pause here and there for the stuff I write.

Besides, it's not like I've decided to **never** learn any other language, it's just
that right now, I'm going to concentrate on doing stuff with Go. Perhaps I'll 
delve deeper into Rust later in the year, or next year.

So with all that out of the way, let me share with you my naïve implementation of
[Project Euler](https://projecteuler.net) Problem 1

> If we list all the natural numbers below 10 that are multiples of 3 or 5, we get 3, 5, 6 and 9. The sum of these multiples is 23.
> 
> Find the sum of all the multiples of 3 or 5 below 1000.

Ok, so first I just did the simple for loop solution

    :::go
    package main

    import "fmt"

    func main() {
        sum := 0
        for i := 0; i < 1000; i++ {
            if (i%3 == 0) || (i%5 == 0) {
                sum += i
            }
        }
        fmt.Println(sum)
    }


Pretty much reads like C, right? Cool. But why would I write C code in Go? I
could just use C, or even Python. So let's make use of these awesome *goroutines* and
split the work a little bit. Now this implementation is a *little* clunky I am sure,
but I'm just starting out, so I'm allowing for some leniency.

{% highlight go %}
package main

import "fmt"

func getSum(start int, end int, c chan<- int) {
	sum := 0
	for i := start; i < end; i++ {
		if (i%3 == 0) || (i%5 == 0) {
			sum += i
		}
	}
	c <- sum
}

func main() {
	sum := 0
    c := make(chan int)
    go getSum(0, 250, c)
    go getSum(250, 500, c)
    go getSum(500, 750, c)
    go getSum(750, 1000, c)

    sum = <-c + <-c + <-c + <-c

	fmt.Println(sum)
}

{% endhighlight %}

Still with me? In that case let's quickly go over what the idea is here.
First I create a channel `c` of type `int` that will communicate with the
goroutine that sums up the relevant numbers. This routine, `getSum`, does
what the `for loop` did in the original implementation, except the result is
sent back to the channel (`c <- sum`).

Then I split the target into 4 (this to me could probably be done more elegantly)
and execute the *goroutines* concurrently. Then the results of the channel are summed
up by `sum = <-c + <-c + <-c + <-c`.

Not quite content with this I decided to do a little timing test. I altered the code
to solve the problem for all numbers under 1,000,000 and do that 100 times. 
The channels are split into 4 as above, but with `0, 250000` and so on.
Running the compiled code with `time euler_001` I checked the execution time:

    Basic for loop implementation: 0:00.48
    Channel implementation: 0:00.19

Not a bad speed up, but also not definitive, as I'm just learning about channels
and goroutines, so I might need to set up a better test bed for this later on.



