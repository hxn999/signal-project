

# Anik Sir/Lecture-1-CSE-219.pdf

Lecture 1: A Little Introduction to Signals

                    CSE 219: Signals and Linear Systems

                                        Anik Saha
                      Adjunct Lecturer, Department of CSE, BUET
A signal is a pattern of change that carries information

        A signal is a quantity whose variation tells us something interesting.

   The independent variable is often time: voice, voltage, speed.
   It can even be space: brightness in an image, temperature over a room.
   We are usually interested in the pattern of change.
Signals: Everything everywhere all at once
Continuous signals are smooth

      Signals that are smooth, defined at every instant
      Examples: microphone voltage, car velocity, temperature over time

                     x (t)

                                 x (t)
                                                                                        value exists
                                                                                         at every t
                                                                                                                    t
Discrete signals have gaps between values

      Signals that are defined only at separated instants
      Digital audio samples, daily temperature log, weekly stock index

x [n]

 x [n]

-5 -4 -3 -2 -1 0                                             n
                  12345
A little convention tells us which time points are allowed

  Continuous signal               Discrete signal

     x (t)                           x [n]

Here, t can be any real value.  Here, n is an integer index.

         x (1)  x (2)                   x [1]  x [2]
       x (0.5)  x ()                 × x [0.5] × x []
Energy is simply a sum of squares

       To measure how "large" a signal is, we square its values and add them up.

Continuous signal           Discrete signal

 E[t1,t2] = t2 |x (t)|2 dt              n2

                    t1      E[n1,n2] =        |x [n]|2

                                        n=n1

The absolute value lets the formula work for both real and complex signals.
Power is energy averaged over the interval

Continuous signal                    Discrete signal

               1     t2 |x (t)|2 dt  P[n1,n2]  =  n2  -  1   +  1    n2  |x [n]|2
P[t1,t2] = t2 - t1                                       n1        n=n1
                    t1

 Divide the energy by the             Divide the energy by
length of the time interval.         the number of samples.
Continuous example: one half-sine has energy /2

Signal                      Energy

                                                         

            sin t, 0  t  ,              E = | sin t|2 dt
  x (t) =
                                                        0
            0, otherwise.                                

x (t)                                      = sin2 t dt
1
                                                        0
         t
                                               
0                                          =.

                                               2

                             The signal is nonzero only from 0
                              to , so we only integrate there.
Average power: let's divide by the interval length

Energy, we already found         Average power
                     
                                 E /2 1
          E=                     P[0,] =  - 0 =       =.
                     2                                   2

Total squared size over 0  t  .

                                 Average squared size
                                   over this interval.
Discrete example: we start from the samples

                    Suppose a discrete-time signal has four samples:
               x [0] = 1, x [1] = -2, x [2] = 2, x [3] = -1.

                    x [n]

   Table of values  2

 n 0123             1
x[n] 1 -2 2 -1

                                                                      n

                        0  1  2  3

                    -1

                    -2
Discrete example: square, add, then average

Energy                                 Average power

             3                         P[0,3]  =  1     3
                                                  4
 E = |x [n]|2                                             |x [n]|2

           n=0                                        n=0

    = |1|2 + | - 2|2 + |2|2 + | - 1|2             10
    =1+4+4+1                                   =
    = 10.
                                                   4

                                               = 2.5.
    Transforming Signals

Signals feel nicer once we are able to move, flip, or stretch them as we wish.
A signal can change both horizontally and/or vertically

          x (t)                   x (2t)                      2x (t)

             A                    A                             2A
                               t
                                                    t                               t
                  a                                                    a
                                       a
value A occurs at t = a                2               At same time t = a;
                                                        value becomes 2A
                                  Same value A

                                  arrives at t  =  a
                                                   2

x(2t): time is compressed, so a  a/2.
2x(t): amplitude is doubled, so A  2A.
Time shift: the whole signal moves left/right

   When t0 > 0
   x (t - t0) is a delay to the right, while x (t + t0) is an advance to the left.

              x (t - t0)
   x (t)

a  a + t0                 t

delay by t0

Same height, same shape but every value simply occurs t0 later.
Shifting shifting: when right and when left?

Delay (shift right): x (t) - x (t - 2)

                     x (t)                                     x (t - 2)

                                                            t                                   t
                             a                                              a+2

Advance (shift left): x (t) - x (t + 3)

x (t)                                                             x (t + 3)

                              t                                                                        t
             a                                                 a-3
Shifting discrete signals: every value moves to a new index

Original: x [n]               delay by  Delayed: x [n - 4]
                             4 samples
                          n                                         n

          0                                        0
Time reversal: mirroring a signal with respect to the origin
Time reversal: mirroring a signal with respect to the origin

            Replace t by -t. A feature at t = a appears at t = -a.

Original signal: x(t)            Reversed signal: x(-t)

                              t                                  t
            0                                 0
Time scaling: compress or stretch?
Time scaling: compress or stretch?

Time scaling changes along the horizontal axis, not the signal height.

Original: x (t)     Compressed: x (2t)  Stretched:  x  (  t             )
                                                          2

                 t                  t                                      t
Can we combine transformations? Yes, sure!

                                 Goal: obtain x (2t + 3)

  x (t) -s-hi-ft-le-ft-b-y 3 x (t+3) --co-m-pr-es-s -al-on-g-ti-m-e -by-2 x (2t+3)

              First create x (t + 3). Then replace its time variable t by 2t.

      The second operation acts on the entire intermediate signal x (t + 3).
Changing the order gives a different answer

  x (t) -s-hi-ft-le-ft-b-y 3 x (t +3) --co-m-pr-es-s-ti-m-e -by-2 x (2t + 3)

   Reverse order

   x (t) --co-m-pr-es-s-ti-m-e -by-2 x (2t) -s-hi-ft-le-ft-b-y 3 x (2(t + 3))

              The shift is now also multiplied by 2, so the result is different.
A simple recipe to obtain
    x (t + ) from x (t)
Step 1  Apply the left/right shift part first:
Step 2                          g1(t) = x (t + )
Step 3
        Apply time reversal only when  < 0:

                                          

                          g2(t) = g1(t),  > 0,
                                    g1(-t),  < 0.

        Finally, scale time by ||:
                        g3(t) = g2 ||t = x (t + )
A simple recipe to obtain x (t + ) from x (t)

                   x (t) - x (t + ) - x (t + )

                   > 0  shift left in 1st step
                   < 0  shift right in 1st step
                   > 1  time compression in 2nd step
            0 <  < 1  time stretching in 2nd step
                   < 0  need to do time reversal before scaling

      Please write the intermediate signal before applying the next operation.
Example: obtain x (-3t + 2) from x (t)

Step 1  Shift left by 2:

                          g1(t) = x (t + 2)

Step 2  Apply time reversal (since -3 < 0):
                        g2(t) = g1(-t) = x (-t + 2)

Step 3  Compress time by 3:
                        g3(t) = g2(3t) = x (-3t + 2)
Visual example: begin with a piecewise signal

             We will transform one simple piecewise signal step by step.

Original signal              Graph of x (t)

         1,     0  t < 1,       x (t)
                1  t  2,    1
                otherwise.
                                                         t
                             012

x (t) = 2 - t,

           
           

         0,
Step 1: shifting left by 2 gives x (t + 2)

            Replace t by t + 2. Every feature moves 2 units to the left.

Shifted signal                Graph of x (t + 2)

             1,  -2  t < -1,    x (t + 2)
                 -1  t  0,                   1
                 otherwise.
                                                            t
                              -2 -1 0

x (t+2) = -t,

               
               

             0,
Step 2: reversing time gives x (-t + 2)

                 Now replace t by -t in the shifted signal x (t + 2).

Reversed signal                 Graph of x (-t + 2)

                    0  t < 1,            x (-t + 2)
                    1  t  2,      1
               t ,  otherwise.
                                                               t
                                    012
                  
                  

x (-t+2) = 1,

                  
                  

               0,
Step 3: compressing by 3 gives x (-3t + 2)

   Finally, replace t by 3t. The reversed signal becomes three times narrower.

Final signal                           Graph of x (-3t + 2)

                      0    t  <  1  ,          x (-3t + 2)
                                 3       1
                3t ,
                      1    t     2  ,                             t
                      3          3         012
                    
                      otherwise.                33
                    

x (-3t+2) = 1,

                    
                    

                0,
Practice 1

                          Starting from x (t), how can we obtain
                                                          t

                                   y (t) = x 3 2 - ?
                                                          2

       Hint: simplify the argument first, then work from the inside outward.
Practice 1: solution

            First simplify: x  3  2  -  t  =      x         6  -  3t
                                        2                         2

 Shift left by 6:

                               x (t) - x (t + 6)

 Reverse time:

                             x (t + 6) - x (-t + 6)

  Compress  time   by  3  :
                       2

                                                         3
                             x (-t + 6) - x - t + 6

                                                         2
Practice 2

                                           Start with
                                          y0(t) = x (t)
   Apply the following operations in the given order and obtain the final signal.

     1. Stretch time by a factor of 2.
     2. Shift left by 3.
     3. Compress time by a factor of 4.
     4. Reverse time.
Practice 2: solution

 Stretch by 2:                                 t
 Shift left by 3:               y1(t) = x 2
 Compress by 4:
                                                    t +3
                      y2(t) = y1(t + 3) = x 2

                   y3(t) = y2(4t) = x  4t + 3              3
                                               = x 2t +
                                       2                     2

 Reverse time:                                 3

                      y4(t) = y3(-t) = x       -2t +
                                                        2
Even and Odd Signals
Even signals are mirror-symmetric about the vertical axis

                 Property: x (-t) = x (t), Example: x (t) = cos(t)
Odd signals flip sign across the origin

                Property: x (-t) = -x (t), Example: x (t) = sin(t)
Every signal has an even part and an odd part. Really!

Even part            1
Odd part   xe(t) = 2 x (t) + x (-t)

                     1
           xo(t) = 2 x (t) - x (-t)
Quick check: does it really work?

Check 1  Show that the even part is truly even:
                            xe(-t) = xe(t)

Check 2  Show that the odd part is truly odd:
                           xo(-t) = -xo(t)

Check 3  Show that, x (t) = xe(t) + xo(t)
Example: begin with a signal that is neither even nor odd

Original signal

                             Graph of x (t)

x (t) =  t + 1, -1  t  1,          x (t)
                                  2
         0,  otherwise.           1

This signal is nei-                                 t
ther even nor odd.         -1 0 1
We first reflect the signal to obtain x (-t)

Time-reversed signal     x (t) and x (-t)
  For -1  t  1,
                         x (-t)               x (t)
     x (-t) = 1 - t
                                 2
 The graph of x (-t) is
 obtained by reflecting          1
  x (t) about t = 0.
                                                  t
                         -1 0 1
Adding and averaging extracts the even part

     Add, then average     Even part: xe(t)

          1                      xe (t )
xe(t) = 2 x (t) + x (-t)          1

          1                                      t
      = (t + 1) + (1 - t)  -1 0 1

          2
      =1
Subtracting and averaging extracts the odd part

  Subtract, then average    Odd part: xo(t)

          1                       xo (t )
xo(t) = 2 x (t) - x (-t)    1

          1                 -1 0          t
       = (t + 1) - (1 - t)      -1  1

          2
       =t


# Anik Sir/Lecture-2-Some-Useful-Signals.pdf

Lecture 2: Some Useful Signals

        CSE 219: Signals and Linear Systems

                           Anik Saha
        Adjunct Lecturer, Department of CSE, BUET
Unit Step and Unit Impulse
            Functions
The discrete-time unit step turns on at n = 0

                                                             

                                                   0, n < 0,
                                 u[n] =

                                                   1, n  0.

                                         Graph of u[n]
                                                               u[n]

                                                                                                                       ···
                                                                     1

                      ···
                                                                                                                               n

                        -6 -5 -4 -3 -2 -1 0 1 2 3 4 5 6
The discrete-time unit impulse is nonzero only at the origin

                                                             

                                                   1, n = 0,
                                 [n] =

                                                   0, n = 0.

     Graph of [n]

             [n]

            1

···                ···           n

-6 -5 -4 -3 -2 -1 0 1 2 3 4 5 6
Unit step function: The sleeping giraffe
Unit impulse function: The giraffe wakes up
Practice

          Use the definitions of u[n] and [n].

Unit step              Unit impulse

         (a) u[1] = ?           (d) [0] = ?
      (b) u[-3] = ?             (e) [4] = ?
                              (f) [-2] = ?
         (c) u[0] = ?
Answers: values of u[n] and [n]

Unit step                        Unit impulse

            u[1] = 1                         [0] = 1
          u[-3] = 0                          [4] = 0
                                           [-2] = 0
            u[0] = 1
                                 Since [n] = 1 only at n = 0.
Since u[n] = 1 for n  0.
Practice: how do shifted signals look?

                         Can we plot each of the signals below?

Shifted steps          Shifted impulses

     (a) u[n - 2] = ?       (c) [n - 2] = ?
     (b) u[n + 3] = ?       (d) [n + 3] = ?
Answers: shifted steps and shifted impulses

u[n - 2]                                  u[n + 3]

   1                                      1
                                   n
                                                    n
     02
                                      -3     0
[n - 2]
                                          [n + 3]
   1
                                   n      1

     02                                             n

                                      -3     0
R1: The impulse is the first difference of the step function
                      [n] = u[n] - u[n - 1]

                      u[n]  1
                 u[n - 1]
[n] = u[n] - u[n - 1]                                                    n
                              0

                            1

                                                                         n
                              01

                                 [n]
                            1

                                                                         n
                              0
R2: A running sum asks whether the impulse is included

                            n    [m]
                            m=-

Case 1: n < 0                           Case 2: n  0

summation interval                    summation interval
                                                            [m]
                       [m]
                                                     spike included
spike not included

     n                      m                      m

                    0                      0  n

n                                     n

     [m] = 0                              [m] = 1

m=-                                   m=-
R2: The running sum of the impulse is the step function

        n

u[n] =       [m]

        m=-

                        Why?

n < 0  the spike at m = 0 is not included
         0

n  0  the spike at m = 0 is included
         1
R3: Delayed impulses can build the step function

    Each delayed impulse [n - k] contributes exactly one sample, at n = k.

     [n]                                                n
[n - 1]   0
[n - 2]
[n - 3]                                                 n
          01

                   n

          0  2

                   n

          0     3
R3: Summing delayed impulses gives the unit step function

u[n] = [n] + [n - 1] + [n - 2] + · · · =        [n  -  k  ]
                                          k =0

Interpretation              The sum: unit step function
                                                       u[n]
      [n]  sample at n = 0
 [n - 1]  sample at n = 1                                                             ···
 [n - 2]  sample at n = 2                       1

          ...  ...                                                                            n
                                                   0123
The continuous-time unit step jumps at t = 0

                                                              

                                                   0, t < 0,
                                 u(t) =

                                                   1, t > 0.

        Graph of u(t)

                             u (t )

            1

               jump

                                                                t

-3  -2  -1  0  1       2             3

The value at exactly t = 0 is usually not important for our signal operations.
The impulse should be the derivative of the step

Discrete time gave us

[n] = u[n] - u[n - 1].

This looks like a difference. In continu-
ous time, we want the analogous idea:

(t) =  du (t )  .

       dt
The impulse should be the derivative of the step

Step                                       Derivative idea

              u (t )                           d
1                                                 u (t )

                                   t           dt
  0
                                       The function is flat every-
                                      where except at the jump.

                                         The jump should be-
                                           come an impulse.
But Oops, we can't differentiate at the origin!

        Away from t = 0, the step is constant, so derivative is 0. At t =
       0, the step jumps instantly, so the ordinary derivative is not defined.

Ordinary derivative                            Impulse notation
                                                          (t )

                       slope 0                          area = 1
         1
slope 0                                                                         t
            problem at t = 0
                                               -2 -1 0  1  2
                                            t
           0

                                               An arrow represents
                                                an ideal impulse.
(*) The derivative of a smoothed step is a tall narrow pulse

We first smooth the jump over a tiny interval , then take the derivative.

 (t )                                                    =  du (t )
                                                              dt

Approximate step u(t)                                                Derivative (t)

                               u (t )                                1   (t )
          1
                                                                     
                                                      t
             0                                                          area 1

                                                                                                                t
                                                                        0
(*) We first replace the instant jump by a very short ramp

  Instead of jumping instantly, let the sig-
nal rise from 0 to 1 over a short interval .

           
           0,      t < 0,
                   0  t  ,
                   t > .
u(t  )  =    t  ,
             
           

           

           

           

           1,
(*) We first replace the instant jump by a very short ramp

                                                  Its derivative

Smoothed step u(t)                                            1   ,  0 < t < ,
                                                  du (t )            otherwise.
                             u (t )                  dt       
       1
                                         (t )  =           =    

short ramp                                                    0,

                                     t

0                                       The steeper the ramp, the
                                        taller the derivative pulse.
(*) Making the transition shorter makes the pulse taller

               u1 (t)                1 (t)
1
                          1

                          1

                       t                        t

0       1                    0               1

               u2 (t)                 2 (t)
1
                           1
                          2

                       t                        t

0    2                       0    2

                          1     3 (t)

               u3 (t)     3
1

                       t                        t

0 3                          0 3
(*) The area under the pulse stays equal to 1

                                                 So the area is

Area of (t)

                                                                 1
                                               - (t) dt =  · 
area  height  1
              

                                            t    = 1.
0
                                               This is the quantity that survives
width                                             as the pulse becomes ideal.
The ideal impulse is the limiting infinitely narrow pulse

          From (t) to (t)

    (t )      0               (t )
area 1                             area 1
0
                   t                       t

                           0

(t) =     du (t )  ,                   t

          dt          u(t) = ( ) d.

                                     -
How to draw impulses with arrows

           The arrow height is not the actual value of the impulse. The
            number beside the arrow just tells us the area or strength.

    Examples of impulse arrows

                                  2(t - 1)
                       (t )

                                               t

-2  -1  0  1  2  3                          4

                    -3(t - 3)
Example: differentiating 2u(t)

d
    2u(t) = 2(t)

dt

Signal: 2u(t)                                    Derivative: 2(t)

                         2u (t )                                  2 (t )
        2                                                    2

                                              t                          area 2
          0
                                                                                                   t
                                                               0
Practice: write the signal using shifted steps

Observe the jumps                          Signal x (t)

   t = 1 : 0  2  +2              x (t)
   t = 2 : 2  -1  -3
   t = 4 : -1  1  +2             2                       x (t)

x (t) = 2u(t-1)-3u(t-2)+2u(t-4)  1

                                                                                            t

                                              1234
                                 -1
Practice: differentiate the jump signal (Example 1.7)

dx (t)  =  2(t - 1) - 3(t - 2) + 2(t - 4)
  dt

                         Derivative x (t)

              x (t)  +2         +2
             2
             1                             upward jump

           -1                               t
           -2
           -3        1   2   3  4

                             downward jump

                         -3
Exponential and Sinusoidal
             Signals
A real exponential either grows, decays, or stays flat

              The basic continuous-time real exponential has the form
                                          x (t) = Ceat,

                             where C and a are real constants.

a > 0: grows                   a = 0: constant                   a < 0: decays

        x (t)                            x (t)                           x (t)
               Ceat                                               Ceat
                                                   C
       C                                C                               C
                            t                                                                 t
                                                              t
Multiplying by a step function keeps only part of a signal

                             The unit step acts like a switch:
          x (t)u(t) keeps the right side of x (t) and removes the left side.

Original exponential e2t                            After multiplying by u(t)

                   x (t)                                                x (t)

                           e2t                                                e2t u(t)

                   1                                zero 1     t
                                                 t
                                                            0
                     0
Shifted steps choose where the exponential begins

                                  Graph of e-tu(t - 2)

                                                   x (t)

                                                                  turns one-t u(t - 2)
                                                     zero before 2

                                                                                                      t
                                                      012345
Practice: what do these exponential-step signals look like?

    Left/right selection       Shifted switches

    (a) etu(-t) = ?       (c) etu(3 - t) = ?
(b) e-tu(t - 2) = ?        (d) e-tu(3t) = ?

Remember: u(3t) = u(t), because 3t has the same sign as t.
   e t u(-t )                                etu(3 - t)

         1                             1     zero after 3 t

                  zero
                                t

           0

                                          0  3

   e-tu(t - 2)                         e-tu(3t) = e-tu(t)

   zero                                            1
                                    t
                                          zero
0  2                                                                              t

                                                     0
A sinusoid repeats after one full cycle

                              x (t) = A cos(0t + ).
    A controls height, 0 controls speed of oscillation, and  shifts the wave.

Period of a continuous-time sinusoid

x (t)           2
A      T0 = |0|

                   A cos(0t + )

                                      t

-A
Larger |0| means faster oscillation

                  cos t

                                                                                                                              t

               cos(2t )

                                                                                                                              t

               cos(4t )

                                                                                                                              t
A rotating point carries both cosine and sine

Unit circle view                    Angle  = 0t gives two signals

                                   cos(0t) and sin(0t)

                     (cos , sin )   They are the horizontal and vertical
   sin                             coordinates of the same rotating point.

                
                                

                 cos 
Euler's formula packages two sinusoids into one expression
                         ej = cos  + j sin 

          With  = 0t               Real and imaginary parts

ej0t = cos(0t) + j sin(0t).         {ej0t} = cos(0t)
                                     {ej0t} = sin(0t)
     One compact expression car-
       ries both cosine and sine.
Changing 0 changes how fast the arrow rotates

                     The signal ej0t moves around the unit circle.
                             Larger |0| means faster rotation.

e j 0 t          e j 20 t            e -j 0 t

                                   

                                                  
    base speed      twice as fast    opposite direction
A real cosine is the sum of two opposite rotations

cos(0t )                                  =  1  e  j  0  t  +  1  e  -j  0t
                                             2                 2

Two rotating arrows                                         What remains is real

                                                            ej + e-j = 2 cos ,
                                                            ej - e-j = 2j sin .
                        1  e  j  0  t
                        2

                                       

                        1  e  -j  0    t
                        2
imaginary parts cancel
Continuous complex exponentials repeat after a full rotation

                                    Period condition

One full rotation                   ej0(t+T ) = ej0t

                                    ej0t ej0T = ej0t

                        same point          ej0T = 1
                              
                                    0T = 2            T0  =  2
    angle 2                                                       .
                                                             |0|
A discrete periodic signal: A sampled cosine

             In discrete time, we only keep the values at integer indices:
                                        x [n] = cos(0n).

        Samples of cos     t
                        4

        x [n]
                       x [n] = cos(n/4)

        1

                                            n

-8  -4      0                 4          8

        -1
Discrete-time periodicity asks for an integer shift

                                 Discrete time periodicity

                                    cos(0n)
                                                          2

                     repeats after every multiple of
                                                          0

                                           2
          But, some multiple N = m must be an integer.

                                           0

             The discrete signal is periodic only if such an integer N exists.
Example: cos(2t) is periodic, but cos(2n) is not

For the continuous signal x (t)                =  cos(2t), the period, T0  =  2  =     .
                                                                              2
But  is not an integer shift in discrete time.

Continuous-time                                   Discrete-time

                                                  repeat                      spacing  
                           cos(2t )                                                     cos(2n)

                                            t     1

                                                                                             n
                                                      012345

                                                  -1
                                                             not an integer
Example:  cos  2  n  repeats every 5 samples
               5

After N = 5 samples, the angle has increased by 2, so it repeats.

                  A periodic discrete-time sinusoid

                     x[n] N = 5     x [n] = cos(2n/5)
                     1

                                                         n

          -5             0       5                   10

                     -1
Practice:  is  3 sin  5  n  periodic?
                      7

                            x [n]  =   3 sin  5  n
                                              7

                   Question                            Hint

Is there a positive integer N so that               We need
                                                    2 N
           x [n + N] = x [n]
         for every integer n?                           =
                                                    0 m
Answer:  3 sin  5  n  is not periodic
                7

         x [n]        =  3 sin  5  n   is not periodic.
                                7

       Apply the test                        Why it fails
                                             For m = 0,
2 2 14 N
    == =                                          14
                                                       m
0 5/7 5 m
                                                   5
        N
  But must be rational                  is irrational, so it can
                                       never be an integer N.
        m
Practice: find the period if it exists

x [n]  =  2 cos  16                     n  +  
                 63                           3

                 Hint

       The phase shift
                
                3

does not affect the period.

Only the coefficient of n matters.
Answer: the fundamental period is N0 = 63

                       x [n]     =   2 cos  16      n   +  
                                            63             3

              Find when the samples line up again

                       2 2 63 N
                              =            ==
                       0 16/63 8 m

So  after  8  cycles,  the  samples  land  exactly  63  steps  later:  8·  63  =  63.
                                                                           8
Thank you!


# Anik Sir/Lecture-3-Linear-Time-Invariant-Systems-and-Convolution.pdf

Lecture 3: Linear Time Invariant Systems and
                       Convolution

                        CSE 219: Signals and Linear Systems

                                            Anik Saha
                          Adjunct Lecturer, Department of CSE, BUET
Systems and LTI Systems

                 Signals go in. Signals come out.
A system transforms an input signal into an output signal

     A system is something that takes a signal and produces another signal.
                           x (t) - system - y (t)

x (t) = u(t)          Continuous-time view   y (t)
                   t                                       t
                                S

                                     system
A system takes a whole signal, not just one number

      Ordinary function: one number goes in, one number comes out

Signal system: one whole signal / function goes
 in, another whole signal / function comes out

x (t)                S                           y (t)
            t                                                t
                    system

whole input signal          whole output signal
Discrete-time systems transform one sequence into another

                 In discrete time, the input is a whole sequence x [n],
                        and the output is another sequence y [n].
                               x [n] - S - y [n]

    Example input-output pair  y [n]
                                                 n
x [n]

n  S
Two Properties that will
   make things easier
Linear: scaling the input simply scales the output

                   If x (t) - y (t), then, a x (t) - a y (t).

x (t)   S                                                      y (t)

2x (t)  S                                                      2y (t)
Linear: adding inputs simply adds outputs

   If x1(t) - y1(t), and x2(t) - y2(t), then, x1(t) + x2(t) - y1(t) + y2(t).

       Separate inputs                       Input together

     x1(t) - y1(t)                x1(t)+x2(t) - y1(t)+y2(t)
     x2(t) - y2(t)
                                       The output is just the sum
Treat the two pieces separately.          of the separate outputs.
Time-invariance
Time-invariant: delaying the input only delays the output

               If x (t) - y (t), then, x (t - t0) - y (t - t0).

     x (t)                           S              y (t)

                              delay     same delay

x (t - t0)                           S              y (t - t0)
An LTI system is linear and time-invariant

Linear                 Time-invariant

ax1 + bx2 - ay1 + by2  x (t - t0) - y (t - t0)

  Why we care: for LTI systems, one special response will
eventually let us compute the output for any possible input.
       A Detour through
           Convolution

Convolution is simply a mathematical operation that appears very
                                  universally.
Convolution is just another operation on two sequences

                a[k ]      13254
                b [k ]
                           2 -1 4 1 3
                        k =0 k =1 k =2 k =3 k =4

     Add                   Subtract                 Convolve

(a + b)[k]               (a - b)[k]               (a  b)[k]

 Add match-             Subtract match-             A different
ing positions.            ing positions.          kind of mixing.
Convolution beautifully appears while multiplying polynomials

First polynomial            Second polynomial

A(z) = 1+3z+2z2+5z3+4z4     B(z) = 2-z +4z2 +z3 +3z4

            13254                       2 -1 4 1 3
            a0 a1 a2 a3 a4              b0 b1 b2 b3 b4

Question: what is the coefficient of z4 in A(z)B(z)?
The coefficient of z4 comes from criss-crossed pairings

            To obtain z4, we collect all products whose powers add to 4.

Pair coefficients whose indices add to 4

        a0 a1 a2 a3 a4

A(z )   1  3   2  5                      4

B (z )  2  -1  4  1                      3

        b0 b1 b2 b3 b4

           a0b4, a1b3, a2b2, a3b1, a4b0

c[4] = 1 · 3 + 3 · 1 + 2 · 4 + 5(-1) + 4 · 2 = 17.
The crossed-pairing rule has a compact formula

                   If

A(z) = a[k]zk,         B(z) = b[k]zk,

                k                      k

then the coefficient of zn in A(z)B(z) is

c[n] = a[k] b[n - k].

               k
Reflection turns crossed pairings into vertical pairings

         The formula b[n - k] means: reflect one sequence, then shift it.

Start with n = 0: compare a[k] with b[-k]

       overlap

a[k ]  13254

b[-k ] 3 1 4 -1 2

                                                                                           k
             -4 -3 -2 -1 0 1 2 3 4

       c[0] = a[0]b[0] = 1 · 2 = 2
Sliding the reflected sequence gives the next coefficients

                       For c[n], we compare a[k] with b[n - k].
                 The shift n decides which products line up vertically.

Now take for example n = 2: compare a[k] with b[2 - k]

a[k ]     13254

b[2 - k]  3 1 4 -1 2

                                                                                   k
            -3 -2 -1 0 1 2 3 4

c[2] = 1 · 4 + 3(-1) + 2 · 2 = 5
At n = 4, the vertical products give the z4 coefficient

             Now compare a[k] with b[4 - k]. All five products line up.

          The same c[4] as before, now as vertical multiply-and-add
                               a[k] 1 3 2 5 4

                          b[4 - k] 3 1 4 -1 2

                                                                                                              k
                                                               01234

                 c[4] = 1 · 3 + 3 · 1 + 2 · 4 + 5(-1) + 4 · 2 = 17
Convolution: Keep the first signal just as is, reflect the
second, slide rightward, find overlaps, then multiply-and-add!
This sliding multiply-and-add operation is convolution

c[n] = (a  b)[n] =        a[k  ]  b[n  -  k]
                    k =-
1. Reflect                     b[k] - b[-k]

                  Turn one sequence around (time-reversal).

2. Shift                    b[-k] - b[n - k]

                  Right shift the reflected sequence to the position n.

3. Multiply, add                   a[k] b[n - k]

                                       k

                  Sum of vertical products give one output value c[n].
Practice: compute the convolution of two short sequences

x [n]                                     h[n]

x [0] = 1, x [1] = 2, x [2] = 1, x [3] = 1 h[0] = 1, h[1] = 1, h[2] = -1, h[3] = 2

                                       n                                         n
0123                                      0123
First reflect one sequence before sliding

                   For convolution, we compare x [k] with h[n - k].
             So the second sequence is first reflected: h[k]  h[-k].

  h[k ]    Reflection of h[k]
h[-k ]
                                  1 1 -1 2
                     reflect around k = 0
         2 -1 1 1

                                                                                    k
         -4 -3 -2 -1 0 1 2 3 4
Slide the reflected sequence: first two output samples

n = 0: compare x [k] with h[-k]              n = 1: shift right by one

x [k ]  1211                                 x [k ]  1211

h[-k] 2 -1 1 1                               h[1 - k] 2 -1 1 1

                                          k                                                   k
     -3 -2 -1 0 1 2 3                                        -2 -1 0 1 2 3

y [0] = 1 · 1 = 1                            y [1] = 1 · 1 + 2 · 1 = 3
The middle positions have the largest overlap

        n=2                                             n = 3: all four samples overlap

x [k ]  1211                                                        x [k] 1 2 1 1
                                                               h[3 - k] 2 -1 1 1
h[2 - k] 2 -1 1 1
                                                                                                             k
                                                     k                                0123
                        -1 0 1 2 3
                                                        y [3] = 1(2) + 2(-1) + 1(1) + 1(1) = 2
y [2] = 1(-1) + 2(1) + 1(1) = 2
As we keep sliding, the overlap becomes smaller

             n=4                                           n=5

         x [k] 1 2 1 1                               x [k] 1 2 1 1

    h[4 - k] 2 -1 1 1                                h[5 - k]  2 -1 1 1

                                                  k                                                  k
                       01234                                         012345

y [4] = 2(2) + 1(-1) + 1(1) = 4                      y [5] = 1(2) + 1(-1) = 1
The last overlap gives the final sample

       n=6                                           Final output

x [k] 1 2 1 1                                 y [n] = {1, 3, 2, 2, 4, 1, 2}

h[6 - k]  2 -1 1 1                              4
                                                3
                                           k    2
       0123456                                  1

y [6] = 1(2) = 2                                                                           n
                                                  0123456
Think: can we shuffle the order?

                      We have defined convolution as
                        (a  b)[n] = a[k] b[n - k].

                                                          k

                But what if we swap the two sequences?

                          Does the order of convolution matter?
Answer: Sure! Convolution does not care about the order

                           ab = ba

                                    Polynomial analogy

                            A(z)B(z) = B(z)A(z)

             Since convolution appeared from polynomial multiplication, swap-
             ping the two polynomials should not change the final coefficients.
But why are we doing all these. . . ?
Why Convolution Matters
      (so very much)!
Our goal: find the output of LTI System for any input signal

              The ambitious problem     y (t)

x (t)

           t  S                      ?                              t

              LTI system

any input                            unknown output

Can we find a systematic method that works for any possible x (t)?
Think: how do we solve a difficult problem for any input?

               Before signals, let us look at a familiar number problem.

                                            Question

                How many positive factors does 72 have?

                         Of course, we could check 1, 2, 3, . . . , 72
                          one by one. But there is a better idea.
The easy pieces are prime powers
                             72 = 23 · 32

 Factors from 23      Factors from 32

20, 21, 22, 23         30, 31, 32
  3+1 = 4              2+1 = 3

 There are 4 choices  There are 3 choices
 for the power of 2.  for the power of 3.
Then we combine the small answers

       Each factor is made by choosing one power of 2 and one power of 3.

                                     Number of choices

     (3 + 1)(2 + 1) = 4 · 3 = 12

                       So 72 has 12 positive factors.
The philosophy: solve simple pieces, then combine

Step 1  Solve for the simplest inputs.
Step 2  Break any input into simple pieces.
Step 3  Combine the small answers gracefully.
The simplest input signal is the impulse function

                                The discrete-time impulse

                                         [n]

                                                                    1
                                                                                                                       n

                               -5 -4 -3 -2 -1 0 1 2 3 4 5

                       It is zero everywhere except at one instant.
The impulse response: poking a sleeping cat. . .
The impulse response is the system's signature

   Given one impulse, the output we observe is called the impulse response.

[n]                 Definition  h[n]
                 n                            n
                       S

                    LTI system

                    [n] - h[n]
An example: one hello can create many echoes
In this toy echo system, the impulse response is a step

               One short input sound produces repeated equal echoes:
                                  [n] - h[n] = u[n].

    Input: one short hello                                    Output: repeated echoes

                           [n]                                                               h[n] = u[n]
                                                                                                                ···
                                                         n
-4 -3 -2 -1 0 1 2 3 4                                                                                                n
                                                            -4 -3 -2 -1 0 1 2 3 4
Think: what does this new impulse response mean?

               [n] - h[n] = nu[n], 0 <  < 1.

      Impulse response

h[n]

1     1, , 2, 3, . . .

                                           ···
                                                                         n
   01234567

What does it mean physically? What if we change ?
Answer:  controls how quickly the echoes fade

        is the fraction of echo strength that survives after each reflection.

        Larger  means slower fading

 = 0.9                                  = 0.3

                                    n                                      n
slower fading                          faster fading

Large : echoes stay longer. Small : echoes die quickly.
Think: what impulse response gives only a delay?

       Suppose a system does nothing except delay the input by 3 samples:
                                        y [n] = x [n - 3].

                          What should its impulse response be?
Answer: a pure delay has a shifted impulse response

     Impulse in, delayed impulse out

[n]                                                      [n - 3]

                                             delay by 3

                                          n                                                        n
0123                                                     0123

                   h[n] = [n - 3]

     Continuous-time version: h(t) = (t - 3).
Now let's send a four-sample input to our toy echo system!

               x [n] = [n] + 2[n - 1] - [n - 2] + [n - 3].

                                                       x [n]
                                                       2
                                                       1

                                                                                                     n
                                                         01234
                                                    -1

          Can we find the output using only the response to one impulse?
Let's first break the input into scaled and shifted impulses!

             Four simple pieces

                                                           2[n - 1]
   [n]

   n                                                                 n

0                               1

                             n     [n - 3]
            2
                                                      n
   -[n - 2]                                  3
LTI tells us the output of each shifted impulse. . .

                             [n] - h[n] = u[n].

Linearity and Time invariance simplifies everything beautifully!

[n] - h[n]  = u[n]

[n - k] - h[n - k] = u[n - k]

a [n - k] - a h[n - k] = a u[n - k]
Each sample creates a shifted copy of the impulse response

      [n] - u[n]                              -[n - 2] - -u[n - 2]

                                           n                                              n
    -1 0 1 2 3 4 5                                 -1 0 1 2 3 4 5

2[n - 1] - 2u[n - 1]                           [n - 3] - u[n - 3]

                                           n                                              n
    -1 0 1 2 3 4 5                                 -1 0 1 2 3 4 5
Linearity lets us add the four outputs

                            Output of the toy echo system

           y [n] = u[n] + 2u[n - 1] - u[n - 2] + u[n - 3].

                                                   y [n]
                                                   3
                                                   2
                                                   1

                                                                                                        n
                                            -1 0 1 2 3 4 5
Any discrete-time input can be built from shifted impulses

        x [n]

···                 ···

                         n

     -2 -1 0 1 2 3

     each sample comes from one scaled shifted impulse

        

x[n] =         x[k] [n - k]

        k =-

The value x [k] becomes the height of the impulse placed at n = k.
The two LTI properties again simplify everything!

Time-      If [n] - h[n], then a shifted impulse gives a shifted
invariant  response:

                               [n - k] - h[n - k].

Linear     If the shifted impulse is scaled by x [k], the output is
           scaled by the same amount:

                          x [k][n - k] - x [k]h[n - k].
Each sample creates a shifted copy of the impulse response

               Suppose the impulse response of the LTI system is h[n].
   Then one input piece x [k][n - k] produces one output piece x [k]h[n - k].

            One input sample at index k

x [k]

                 S

              n  LTI                                                        n
                                                      k
k
                                         x [k]h[n - k]
x [k][n - k]
Now add the responses from all samples

Input decomposition becomes output summation

               x [n] =    x [k][n - k]
Therefore, y [n] =
                        k

                          x [k]h[n - k]

                        k

Every term x [k][n - k] contributes one term x [k]h[n - k] to the output.
Convolution Returns!!!

The LTI input-output formula

y[n] =                        x[k] h[n - k]

                        k =-

y [n] = (x  h)[n]
The bridge thus completes!

1  Find the system's response to the simplest input.

   [n] - h[n]. This h[n] is the impulse response.

   Break any input signal down into shifted impulses.

2  x [n] = x [k][n - k].

   k

   Shift, scale, and add the impulse responses.

3  y [n] = x [k]h[n - k] = (x  h)[n].

   k
Please try listening to convolution outputs here!


# Anik Sir/Lecture-4-Convolution-Causality-and-Stability.pdf

Lecture 4: Convolution, Causality, and Stability

                         CSE 219: Signals and Linear Systems

                                             Anik Saha
                           Adjunct Lecturer, Department of CSE, BUET
Recall: Keep the first signal just as is, flip the second, slide
rightward, find overlaps, then multiply-and-add!
Recall: discrete-time convolution is sliding multiply-and-add

For two discrete-time signals x [n] and h[n], their convolution is

                            

       y [n] = (x  h)[n] =        x [k] h[n - k].

                            k =-

       What the formula is saying

x [k]  multiply  h[n - k ] add over k                               y [n]

       For each fixed n, the sum produces one output sample y [n].
Convolution gives a whole output signal, one value at a time

Sweep over the input index k                       Fix one output index

                          x [k ]

                                                           y [n]
                                                                       fixed n = 3

···                            ···                                      y [3]

     -4  0                               k     ···                          ···
                           4
                                                                  0                     n
                                                                     3

         sweep over all k

            y [3] =                         x  [k  ]  h[3  -  k]
                           k =-
For fixed n, h[n - k] is made by reflect-then-right-shift

     h[k ]                               k

  h[-k ]                        0     3

                            -3                                  k
                                0
h[2 - k]
                                                 h[0] now sits at k = 2

                                         k

                                0  2
The continuous-time version replaces the sum by an integral

                   For continuous-time signals, the idea is the same:
                      reflect, shift, multiply, and add continuously.

                              Continuous-time convolution

                                                              

                y (t) = (x  h)(t) = x ( ) h(t -  ) d

                                                             -
For a fixed t, sweep along  and integrate along the overlap

Fix t, then slide h(t -  ) along the  -axis

   x ( )
                                 h(t -  )

   overlap

                                             

a  0 t-d  b                    t -c

          slide as t changes

        For this one fixed t,

                    

   y (t) = x ( ) h(t -  ) d

                   -
Discrete and continuous convolution follow the same recipe

1  Choose the output location.

   For discrete time, choose n. For continuous time, choose t.

   Reflect and shift the second signal.

2  Discrete: h[k]  h[-k]  h[n - k]. Continuous:

   h( )  h(- )  h(t -  ).

3  Multiply where they overlap, then add.

   Discrete: sum over k. Continuous: integrate over  .
Please try this demo on computing convolutions!
Practice Problems on
      Convolution
Practice (Example 2.2)

For the two signals below, compute

                                                              

y [n] = x [n]  h[n] =                                               x [k]h[n - k].

                                                              k =-

             Input x [k]                                            Impulse response h[k]

                                2                                   1               h[k ]

                               x [k ]                                                                                      k
                                                                -3 -2 -1 0 1 2 3
                   0.5
                                                           k

-3 -2 -1 0 1 2 3
Answer setup: h[n - k] is the reflected signal shifted by n

                  For each fixed n, draw h[n - k] as a function of k.

     h[k ]                                                    k
  h[-k ]    -2 -1 0 1 2 3
h[n - k]
                                     shift by n
                                                              k

            -2 -1 0 1 2 3

                                                              k
                              n-2n-1 n
Answer: start sliding h[n - k] past x [k]

     x [k ]   n < 0: no overlap
h[n - k]
                                             2
                                      0.5

                                                                      k

                                                 y [n] = 0

                                                                      k
             -4 -3 -2 -1 0 1 2 3 4

For n < 0, the two signals do not share any nonzero overlap of k
Answer: start sliding h[n - k] past x [k]

     x [k ]      n = 0: one overlap
h[0 - k]
                                             2
                                      0.5

                                                                      k

                            overlap y [0] = 0.5 × 1 = 0.5

                                                                      k
             -4 -3 -2 -1 0 1 2 3 4
Answer: when the signals overlap more, the sum grows

     x [k ]      n = 1: two overlaps
h[1 - k]
                                             2
                                      0.5

                                                                      k

                                           y [1] = 0.5 + 2 = 2.5

                                                                      k
             -4 -3 -2 -1 0 1 2 3 4
Answer: when the signals overlap more, the sum grows

     x [k ]   n = 2: still two overlaps
h[2 - k]
                                             2
                                      0.5

                                                                      k

                                           y [2] = 0.5 + 2 = 2.5

                                                                      k
             -4 -3 -2 -1 0 1 2 3 4
Answer: after the last overlap, the output returns to zero

     x [k ]  n = 3: one overlap
h[3 - k]
                                             2
                                      0.5

                                                                      k

                                                  y [3] = 2

                                                                      k
             -4 -3 -2 -1 0 1 2 3 4
Answer: after the last overlap, the output returns to zero

        n > 3: no overlap again

             2

x [k ]  0.5

                                 k

                                 y [n] = 0

h[n - k]

                                                                                 k
                   -4 -3 -2 -1 0 1 2 3 4 5

After n = 3, the sliding signal has passed the support of x [k]
Answer: final convolution output

                                                         
                                                    0.5, n = 0,
                                                         
                                                         
                                                    2.5, n = 1,
                                                         
                                                         
                                   y [n] = 2.5, n = 2,
                                                         
                                                    2, n = 3,
                                                         
                                                         
                                                    0, otherwise.

                                                           y [n]
                                                                    2.5 2.5
                                                                                      2

                                                           2

                                                           10.5

                                                                                                           n
                                           -2 -1 0 1 2 3 4
Practice (Example 2.3)

                           Let 0 <  < 1. Compute
                y [n] = x [n]  h[n], x [n] = nu[n], h[n] = u[n].

     Input x [n] = nu[n]                Impulse response h[n] = u[n]

     1                                                            h[n]      ··
                             x [n]
                                        1

···                                     ······ n

     0  5                           10                      0  5        10
First understand how h[n - k] looks like

      Reflect h[k], then shift it by n    ···

h[k] · · ·                                       k

                                   0

···                                ··· k
           h[-k ]
                ···  0
                                                edge at k = n
        h[n - k]
                                                         ··· k

                                                         n
For n < 0, there is no overlap

                         No common nonzero k

                               1

x [k]                                                        ···
       ···                                                           k

            ···          n<0                  y [n] = 0
h[n - k]                              0
                                                             k
                     -5
                                         5    10         14
For n  0, the overlap is from k = 0 to k = n

                                    1                                 ···
                                                                              k
x [k]
       ···

                                       0k n

                                                                k =n

            ···
h[n - k]

-4               0                     5  8 10                                     k
                                                                      14

Overlap  x [k]h[n - k] = k , 0  k  n.
Therefore the product is just the overlapping part of x [k]

Product sequence for n  0

                 x [k]h[n - k] n

···                 n                              ···
                                                           k
              0
                 5

                                        

                                    k, 0  k  n,
                 x [k]h[n - k] =

                                    0, otherwise.
Now sum the product over all k

            Only the overlap region contributes to the convolution sum.

For n  0

         

y [n] =        x [k]h[n - k]

         k =-

      n

= k

         k =0

= 1 +  + 2 + · · · + n.
The finite geometric sum gives the final answer

For 0  <    <  1, 1 +  + 2 + · · · + n        =  . 1-n+1
                                                   1-

               Final convolution output

                         1  - n+1  ,  n  0,
                            1-        n < 0.

                       

                       

                       

            y  [n]  =

                       

                       0,
The output rises and approaches a limiting value

                             Shape of y [n]

                    1 y [n]                              ···

                  1-

y [n] =  1 - n+1  u[n]

         1-

         ···                                                  n

                         0   5               10  15  20
Practice (Example 2.5)

     y [n] = x [n]  h[n],   Compute           h[n] = u[n].
                            x [n] = 2nu[-n],

     Input x [n] = 2nu[-n]     Impulse response h[n] = u[n]

                  1                                         h[n]  ·
     x [n]
                                                  1

···                            · ···· · n

     -4              0      4                 -4     0      4
First understand how h[n - k] looks

         Reflect h[k], then shift it by n            ···

h[k] · · ·                                                  k

                                                  0

            ···                          ··· k
  h[-k ]
                 0
            ···                      edge
h[n - k]
                                         ··· k

                                        n
For n < 0, the overlap stops at k = n

        x [k]                                  1            ···
               ···                k =n                              k

overlap: k  n                                                  k

               ···            -4  0               4         8
   h[n - k]
                              x [k]h[n - k] = 2k for k  n.
                          -8

        For n < 0,
For n  0, all nonzero samples of x [k] overlap

        x [k]                     1
               ···
                                                             ···
overlap: k  0                                                                     k
                                                        k =n
               ···
   h[n - k]                                                    k

                          -8  -4  0  4                      8

        For n  0,             x [k]h[n - k] = 2k for k  0.
For n < 0, the sum stops at k = n

Case 1: n < 0

         

y [n] =        x [k]h[n - k]

         k =-

         n

=              2k .

         k =-

    n

       2k = 2n + 2n-1 + 2n-2 + · · · = 2n+1.

k =-
For n  0, the sum includes all left-sided samples

      Case 1: n  0

               

      y [n] =        x [k]h[n - k]

               k =-

               0

      =              2k .

               k =-

0 2k = · · · + 1 + 1 + 1 + 1 = 2.
                  842
k =-
The output is left-sided exponential, then a constant

            Final answer

                 2n+1, n < 0,
        y [n] =

                 2, n  0.

            y [n]         y [n]  ···
            2
            1             4              n
                                 8
···     -4  0

    -8
Practice (Example 2.6)

                                 Let a > 0. Compute
              y (t) = x (t)  h(t), x (t) = e-atu(t), h(t) = u(t).

Input x (t) = e-atu(t)                             Impulse response h(t) = u(t)

                 1                                    u (t )       ···
                             e-at u(t)
                                                   1
···
                                        ···        ···
                   0                            t                                                                  t
                                                                      0
First understand how h(t -  ) moves

       Reflect h( ), then shift by t           ···

h( ) · · ·                                              

                                   0

···                         ··· 
  h(- )
                 0
            ···
h(t -  )                                 edge

                                               ··· 

                 0                   t
For t < 0, there is no overlap

           No common nonzero           ··· 

                                    1

x ( )
       ···

                                    0

            ···                          y (t) = 0
h(t -  )
                                                                         
                             t<0 0
                                    y (t) = 0.
          No overlap 
For t > 0, the overlap is 0    t

    x ( )         1                       ··· 
             ···
                  0                                  
             ···
h(t -  )              0 t            0    t.

                  0               t

Overlap  x ( )h(t -  ) = e-a ,
Now integrate only over the overlap

                                    

For t > 0, y (t) = x ( )h(t -  ) d

                                  -

        t

= e-a d 

      0

= - 1 e-a t
      a
                                     0

   1  1 - e-at                          .
=
a

For t < 0, there is no overlap, so y (t) = 0.
The output gradually rises to 1/a

                                   1  1 - e-at  u (t ).
                          y (t) =
                          a

                  y (t)                         ···

                       1              y (t)     =        1    -  e-at )u(t)
                       a                                  (1
                                                         a
···
                                                              t
                    0

                                                                              1
As t increases, the overlap grows, so the integral rises toward .

                                                                              a
Property: Convolution distributes over addition

                      If one signal is a sum of two simpler signals,
                        we may convolve the two parts separately.

          x [n]  h1[n] + h2[n] = x [n]  h1[n] + x [n]  h2[n].
            x1[n] + x2[n]  h[n] = x1[n]  h[n] + x2[n]  h[n].
Practice (Example 2.10)

                               Compute

y [n] = x [n]  h[n],  x [n] =     1  n                 h[n] = u[n].

                                  2   u[n] + 2nu[-n],

        Input x [n]                             h[n] = u[n]

        2                                                  1         ···

       2nu[-n] 1      1  n        ··· n  ···                               n
                      2
···                       u[n]                               0

-6  -3            0   3        6
Oops, different input expressions on the left and right side!

             formula changes

     2k                       1k

···                           2                       ···

                                                           k

             0

     x[k] =  2k u[-k] +       1k
                                   u[k] .
                              2

             left-sided part
                                    right-sided part

             So, we split it first.
Split the problem into two easier ones!

Split x [n], then convolve separately

x [n] = x1[n] + x2[n],              1n   x2[n] = 2nu[-n].
                        x1[n] = 2 u[n],

y [n] = x[n]  h[n]
     = x1[n]  h[n] + x2[n]  h[n]
     = y1[n] + y2[n].

Each part is one we already know how to do.
The two smaller convolutions have simple answers

         Left-sided part       Right-sided part

x2[n] = 2nu[-n], h[n] = u[n].              1n   h[n] = u[n].
        y2[n] = x2[n]  h[n].   x1[n] = 2 u[n],
                2n+1, n < 0,
                               y1[n] = x1[n]  h[n].
      y2[n] =
                2, n  0.       y1[n] = 2 - 2-n u[n].
Now add the two outputs

Final expression

y [n] = y1[n] + y2[n].

                         2n+1,  n < 0,

y [n] =                  4 - 2-n, n  0.

The left side rises toward 1, then the right side rises toward 4.
The output approaches 4 on the right

                  Sketch of y [n]

                  y [n]

                  4                      ···

                  3         4 - 2-n              n

                  2

         2n+1     1

···           -3     0   3            6

     -6

         y [n] =  2n+1,     n < 0,

                  4 - 2-n, n  0.
Practice: convolve two one-sided exponentials

                          Find y (t) = x (t)  h(t), where
                           x (t) = etu(-t), h(t) = e-tu(t).

       x (t) = etu(-t)                                    h(t) = e-tu(t)

                                 1                        1                  ···
                    et                                                  e-t         t

···                                                         0
                                                       t
                                   0
Answer: here the second signal is not just a step

                                   First find the overlap

                       x ( ) = e u(- ) = x ( ) = 0 only for   0.
             h(t -  ) = e-(t-)u(t -  ) = h(t -  ) = 0 only for   t.

               Therefore the overlap is   min(0, t). On the overlap,
                            x ( )h(t -  ) = e e-(t-) = e-t e2 .
Case 1: for t < 0, the overlap ends at  = t

            Overlap: - <   t

         x ( )                         1

                ···                                             
                                         0

                     overlap

                              1

         h(t -  )

                   ···
                                                                                 

                                 t     0

y (t) =  t                          t e2 d  = 1 et ,                               t < 0.
                                          2
            e e-(t- ) d  = e-t

         -                          -
Case 2: for t  0, the overlap ends at  = 0

            Overlap: - <   0

         x ( )                     1

                ···                                               
                                     0

                     overlap

                                      1

h(t -  )                                           

            ···

                                   0     t

y (t) =  0                      0 e2 d  = 1 e-t ,                   t  0.
                                      2
            e e-(t- ) d  = e-t

         -                      -
Final answer: a two-sided decaying exponential

                      1  e  t  ,     t < 0,
                                     t  0.
                    
                    

        y  (t )  =    2
                      1
                         e-t      ,
                      2
                    

                    y (t)

     1  e  t        1                1  e-t
     2              2                2

···                                          ···  t

                       0
Causality and Stability
Causality: No Time Travel Please!!!
For an LTI system, causality is visible from h(t)

                    The impulse response h(t) shows what the sys-
                   tem does after we poke it with (t) at t = 0.

Causal                                                 Noncausal

                      h(t )                     h(t )  effect before cause

nothing before                               t                                                     t
                   0                                                0
                      for t < 0.
   h(t) = 0                                     h(t) = 0 for some t < 0.
Testing causality: the impulse response must be zero before 0

                           For continuous-time LTI systems

                 causal  h(t) = 0 for all t < 0

                                   Discrete-time version

                              causal  h[n] = 0 for all n < 0
Stability means bounded input gives bounded output

            A stable system does not turn a bounded input (value  B
            always) into an output that shoots up to infinity and beyond.

Stable behavior

B   bounded output     Unstable behavior

                    t            keeps growing

                                                                   t

-B
Stability depends on the size of the impulse response!

                               Intuition in continuous case

                                              

                   y (t) = h( )x (t -  ) d, yes, we shuffled it!

                                             -

                                     If the input is bounded, say
                           |x (t)|  B for all t, then, |x (t -  )|  B.

                                                                          

                                 |y (t)|  B |h( )| d.

                                                                        -
Stable LTI system: The total area under |h(t)| must be finite

Continuous-time LTI stability test

stable      |h(t)| dt < 

         -

Discrete-time version

         

stable        |h[n]| < 

         n=-
Two simple little problems

                      Assume an LTI system with impulse response h(t).
  1. If the system is causal, is it possible for h(t) to be periodic?
  2. If the system is stable, is it possible for h(t) to be periodic?
Answer 1: Causality vs Periodicity

If h(t) is periodic and nonzero somewhere for t > 0, then the same nonzero value
repeats backward:

                              h(t0) = h(t0 - T ) = h(t0 - 2T ) = · · ·
Eventually, t0 - kT < 0, which contradicts causality.

                                                  h(t )
                            forced into t < 0 nonzero

                                                                                      t
                                                    0

   Therefore, only the trivial impulse response h(t) = 0 can be both causal and periodic.
Answer 2: Stability vs Periodicity

A nonzero periodic impulse response repeats forever. So if one period has positive area
A under one period, then over infinitely many periods,

                                             

                                    |h(t)| dt = A + A + A + · · · = .

                                           -

      |h(t )|

A  A  A                             A

                                         t
      0

Therefore, only the trivial impulse response h(t) = 0 can be both stable and periodic.
Practice: decide causality and stability

For each impulse response, decide whether
    the LTI system is causal and stable.

           System 1           System 2

h1(t) = e2tu(-2 - t)  h2(t) = te-tu(t)
Answer 1: h1(t) = e2tu(-2 - t) is not causal

Support of h1(t)

u(-2 - t) = 1  -2 - t  0  t  -2.

           t  -2              impulse time

···                                         ···
                                                            t
   vertical scale enlar-ge2d         0

h1(t) is nonzero before t = 0. So the system is not causal.
Answer 1: h1(t) = e2tu(-2 - t) is stable

      Stability test

                    -2  e2t dt.

      |h1(t)| dt =

   -                -

-2           1 e2t -2 = 1 e-4 < .
             2 - 2
   e2t dt =

-

Therefore, the system is stable.
Answer 2: h2(t) = te-tu(t) is causal

Support of h2(t)

    u(t) = 0 for t < 0.

impulse time
                     te-t u(t)

···                                   ···
                                              t
                   0

h2(t) is zero before t = 0. So the system is causal.
Answer 2: h2(t) = te-tu(t) is stable

   Stability test

      
   |h2(t)| dt = te-t dt.

-  0

    

       te-t dt = 1 < .

   0

Therefore, the system is stable.
Problem: how much delay makes it causal?

               Let x (t) = e-2tu(t + 2), and y (t) = x (t - a).
                 Find the minimum value of a so that y (t) is causal.

starts at t = -2
                          x (t) = e-2t u(t + 2)

nonzero before 0

                                                 t

-2                0  2

How far must we shift this signal to the right?
Answer: shift it right by at least 2

       starts here

x (t)

                                      t

       -2           0
           right shift by a

                    causal start

y (t) = x (t - a)

                                                                                                                          t
                                                                     0

For causality, -2 + a  0, so a  2.
Thank you!


# Anik Sir/Lecture-5-Fourier-Series-Let_s-Look-Inside.pdf

Lecture 5: Fourier Series - Let's Look Inside!

                       CSE 219: Signals and Linear Systems

                                          Anik Saha
                         Adjunct Lecturer, Department of CSE, BUET
       Fourier Series

Breaking complicated periodic signals into simple waves.
Can we break down a periodic signal into simple sine and
cosine waves? Yes, we always can!

                      x (t)                          tsin(0 t )
                                                     tsin(20 t )
                                       split into    tcos(30 t )

                                                  t

            TT
complicated periodic signal

complicated periodic signal = sum of simple periodic waves.
Why this idea is useful

1  Some problems are easy for simple waves.

   A sine-shaped vibration or temperature pattern.

   Real initial shapes are usually not simple.

2  A string can be plucked into a strange shape. A metal rod

   can have an arbitrary initial heat pattern.

   Fourier series gives the bridge.

3  Break the random shape into simple waves, solve each simple

   wave, then add the answers.
Example: how will a plucked string move?

                        predict

initial shape f (x )             future shape u(x , t)

    released from rest

We want the whole function u(x , t): shape
  of the string at every position and time.
Please try this visualization on vibrating strings!
Another example: how does heat smooth out?

hot  cold                   wait     smoother

initial temperature f (x )        temperature u(x , t)

  A simple sinusoidal heat pattern is easy to predict. A random
heat pattern becomes manageable after breaking it into sinusoids.
Please try this visualization on heat diffusion!
The repeated strategy: solve the easy waves, then add

                        Break the initial shape into simple waves.

1

                                         f (x ) = wave1 + wave2 + wave3 + · · ·

2  Let each simple wave evolve by itself.

   Add the evolved waves back together.

3  The complicated future behavior comes from adding many

   simple future behaviors.
Bell, bell, bell! Who's there?

          Bell A       A bell analogy           Bell C
   rings every 2 min                     rings every 5 min
                             Bell B
                      rings every 3 min

                                                            time

0  6                  12        18       24       30

   the combined pattern repeats after 30 minutes

The combined period is a common multiple of the individual periods.
                                lcm(2, 3, 5) = 30.
The same story, but viewed through frequency

        Periods         =         Frequencies

  2, 3, 5 minutes          30, 20, 12 times/hour
Tcombined = 30 minutes         f0 = 2 times/hour

The individual frequencies are multiples of the combined frequency:
                 30 = 15f0, 20 = 10f0, 12 = 6f0.
For a signal with period T , the fundamental frequency is 0

                                                                    x (t)

                t

T            T

          2
   0 = T
Therefore, the allowed building blocks are k0

negative harmonics       k =0      positive harmonics
  rotate backward   constant part    rotate forward

                                                       frequency

-40 -30 -20 -10 00 10 20 30 40

For a period-T signal, we use frequencies
      . . . , -20, -0, 0, 0, 20, . . .
     or simply k0, where k  Z.
Instead of sines and cosines, we use complex exponentials

Complex exponentials package sine and cosine together

ej0t = cos(0t) + j sin(0t)
              e j 0 t

cos(0 t )                                 j sin(0t)

           one object carries both parts
So the Fourier series will look like this

Complex exponential Fourier series

                                     ak ejk0t

                      x (t) =

                               k =-

         e jk 0 t     ×                        ak
the k-th simple wave
                                 how much of that wave
Now the question is: what are the coefficients?

Each coefficient tells us how much of one frequency is present

               ak ejk0t

x (t) =

         k =-

                                                              frequency

-40 -30 -20 -10 00 10 20 30 40
          ak = 0: frequency absent ak = 0: frequency present
Example: a cosine already contains two complex waves

Using Euler's formula

cos(0t )     =   1 ej0t  +  1 e-j0t
                 2          2

1                1

2                2

                                           frequency

-30 -20 -10  00  10         20  30

only the -0 and +0 components are present
A small detour: averaging a rotating exponential

     rotates               does not rotate

average cancels to 0         average remains 1

                         

1  T ejk0t dt         =  1, k = 0,
T                        0, k = 0.
Finding a0 is easy, just take the average of x (t)!

x (t) = · · · + a-1e-j0t + a0 + a1ej0t + a2ej20t + · · ·

a-1 e -j 0 t  a0           a1 e j 0 t                   a2 e j 20 t

average 0     survives     average 0                    average 0

              So a0 is just the average over a period:

                        1
              a0 = T         x (t) dt.

                           T
How can we find a1? Make the a1 term stop rotating!

      x (t) = · · · + a-1e-j0t + a0 + a1ej0t + a2ej20t + · · ·

                            Multiply by e-j0t
x (t)e-j0t = · · · + a-1e-j20t + a0e-j0t + a1 + a2ej0t + · · ·

Now a1 is non-rotating. So averaging over one period extracts a1.

       1    x (t)e-j0t dt.
a1 = T
          T
General idea: move the desired coefficient to zero frequency

before                                                          ak  frequency
 after                                                              frequency
        -30 -20 -10 00 10 20 30

                     multiply by e-jk0t

                                          ak

        -30 -20 -10 00 10 20 30

Shift ak to zero frequency, take average. Everything else rotates away.
The coefficient formula

Fourier series coefficient

       1                   x (t)e-jk0t dt
ak = T
                         T

The integral can be taken over any one full period.

       2                 k = 0, ±1, ±2, . . .
0 = T ,
Please try building Fourier Series as you wish!
Practice Problems on Finding
       the Fourier Series
Example: can we find the Fourier series without integrating?

                                                                 T0   =  2
x (t) = 1 + sin(0t) + 2 cos(0t) + cos 20t + 4 ,                             .
                                                                         0
                                                          x (t)

                                                                      t

-2T0  -T0  0                            T0                       2T0

Do we really need to compute ak  =  1   t0+T0  x  (t )e -jk 0 t       dt ?
                                    T0  t0
Answer: Yes! The Fourier components are already visible

sin  =  ej - e-j  ,                   cos  =  ej + e-j   .

        2j                                      2

Components at frequencies +0 and -0

                               1  ej0t - e-j0t  + ej0t + e-j0t
sin(0t) + 2 cos(0t) = 2j

            =        1                ej0t +          1  e-j0t .
               1+                               1-
                                  2j               2j
The phase-shifted cosine gives the second harmonic

Components at frequencies +20 and -20

                  =  1  e  j  (20  t  +     )  +  1  e  -j  (20 t +     )
cos 20t + 4                              4                           4

                     2                            2

                  = 1 ej/4 ej20t + 1 e-j/4 e-j20t .
                        2                                   2

Do not forget the constant term

1 = 1 · ej00t                            =              a0 = 1.
Collect terms with the same rotating frequency

    Complex exponential Fourier series

              2                          j
               (1                   1+
   x (t) =  4      -  j )e-j20t  +     2    e-j0t + 1

                       j              2 (1 + j)ej20t .
            + 1-
                      2   ej0t +    4

k           -2            -1 0 1              2

      2                   j            j2
ak          (1 - j) 1 + 1 1 -                  (1 + j)
    4                     2            2    4
       Magnitude spectrum: |ak|

                     |ak |     

           5                     5

           2            1      2

    1                                    1

    2                                    2

                                                  k

-3  -2     -1        0         1         2     3

           Phase spectrum: ak

                     ak                  

           tan-1  1                      4
                  2

-3     -2     -1        0         1         2            k
                                                  3

                            -  tan-1  1
       4                              2
    -
Practice: Fourier series of a periodic square wave



         1,  |t| < T1,         x (t + T ) = x (t),         2
x (t) =                                             0 = T .
0, T1 < |t| < T /2,

                        x (t)
                        1

···          -T         -T1 0 T1  T                     ···

      -2T                                                         t
                                                    2T

Find the complex exponential Fourier series coefficients ak.
Only the nonzero part contributes to the integral

Choose one convenient period: -T /2 < t < T /2

                                                x (t)

                                               1

                                         t

-T /2 -T1        T1                T /2

       1  T /2 x (t)e-jk0t dt = 1   T1 e-jk0t dt .
ak = T               T
          -T /2                    -T1

Outside -T1 < t < T1, the signal is zero.
For k = 0, evaluate the short integral

Coefficient for k = 0

       1   T1 e-jk0t dt
ak = T
          -T1

   1      e-jk0t T1
=         -jk 0 -T1

   T

= 2 sin(k0T1)
       T k0

= sin(k0T1) .
        k
For k = 0, the coefficient is just the average value

The constant coefficient

       1  T1 1 dt = 2T1 .
a0 = T         T
          -T1

The average value is just:

time spent at height 1 = 2T1 .
total period      T
Frequency-domain picture of the square wave, when T1 = T /4

             a0  =  1               sin(k /2)
                     ,        ak =             , k = 0.
                    2                  k

                                       ak

                                           1

                                    1      2   1

                                               

···                                                             ···

     -7  -5            --331        -1 0 1        -331   5  7
Problem: Fourier series of a repeated triangular ramp

     
     t ,               0  t < 1,
     

     x (t) = 3 - t                 x (t + 3) = x (t).

          2         ,  1  t < 3,
     

          x (t)
                             T =3

          1

···                                                                ···

                                                                        t

-3        0            1           3  4                            6

     Find the complex exponential Fourier series coefficients ak.
Let's first find a0: the average height over a period

               13
        a0 = 3 0 x (t) dt

11                    3 3-t
a0 = 3     t dt +         dt
                      2
        0          1

11                 1
= +1 = .
32                 2

                                                    1
So the average height over one period is .

                                                    2
Same a0, seen geometrically

x (t)
1

              triangle

0            1                             t
                                   3

                             1        3
area over one period = · 3 · 1 = .
                             2        2

a0  =  area  over a period   =  3  =  1
              period            2       .

                                3     2
For k = 0, split the coefficient integral

       1      3                  0 =       2
ak = 3                                       .
                x (t)e-jk0t dt,            3

             0

       1     1              3 3 - t e-jk0t dt .
ak = 3                      12
              te-jk0t dt +

          0
Evaluate the two pieces

                         For k = 0,

     1                   dt   =    e -jk 0  +  1 - e-jk0
                                 -              (jk0)2 .
       te -jk 0 t
                                    jk 0
    0

 3  3 - t e-jk0t         dt   =  e -jk 0  +  e-jk0 - e-j3k0
1     2                           jk 0           2(jk0)2 .

           2                     e-j3k0 = e-j2k = 1.
Since 0 =                  ,
                         3
The final simplification

The                       1     terms cancel:

                          jk 0

       1 1 - e-jk0 e-jk0 - 1
ak = 3 (jk0)2 + 2(jk0)2

1 1 - e-jk0
=·                                   .
   3                      2(jk 0 )2

Since (jk0)2 = -k202,

                                 e-jk0 - 1
                          ak = 6k202 .
Final answer

              Fourier series coefficients

                                   1
                            a0 = 2

                     e-jk0 - 1  k = 0,  0 =  2
              ak = 6k202 ,                     .
                                             3
Please try this visualization on Fourier Series!
Please also try drawing any 2D closed curve!
*A beautiful intuition!
*A coordinate system turns a point into numbers

                                               y

                                                              point (3, 2)

                                                                                     2 steps along y
                                                                                                    x

                                                       3 steps along x

                        How much of each direction do we need?
*Functions can also be presented with coordinates

Example: all functions of the form f (t) = a + bt

f (t) = a · 1 + b · t

basis functions        coordinates

    1, t                  (a, b)

3 + 2t  (3, 2)
*More axes let us describe more complicated functions

                            f (t) = a0 + a1t + a2t2 + a3t3 + · · ·
                                       Now the axes are

                                    1, t, t2, t3, . . .

                                 The coordinates of f (t) are
                                       (a0, a1, a2, a3, . . .).
*Even et has coordinates in this system

                      et = 1 + t + t2 + t3 + t4 + · · ·
                                       2! 3! 4!

                                 So in the coordinate system
                                        1, t, t2, t3, . . .

                        we may think of et as having coordinates
                                                11

                                       1, 1, , , . . . .
                                               2! 3!
*Fourier series simply chooses a different coordinate system

     Polynomial axes                     Fourier axes
   1, t, t2, t3, . . .
                                 . . . , e-j0t , 1, ej0t , ej20t , . . .
f (t) = a0 + a1t + a2t2 + · · ·
                                          

                                 x (t) =        ak ejk0t

                                          k =-
*Example: where is cos(0t) in Fourier coordinates?

     cos(0t )  =  1 ej0t  +  1 e-j0t
                  2          2

     1            1

     2            2

···                                   ···        k

     -3 -2 -1 0   1          2  3

     Only k = -1 and k = 1 are present.
        All other Fourier coordinates are zero.
*import projection from linear_algebra

         Vectors                                         Signals

coordinate along u = v · u              coordinate along ejk0t = x (t), ejk0t

                          v             projection = Fourier coefficient ak

                                     u

Same idea: find how much of one axis is present.
*For signals, dot product becomes an average over one period

                  1  x (t)z(t) dt
x (t), z(t) =
               TT

For the k-th Fourier axis,

z (t) = ejk0t        z (t) = e-jk0t .

       1         x (t)e-jk0t dt
ak = T
               T
Thank you!


# Anik Sir/Lecture-6-Properties-of-Fourier-Series.pdf

Lecture 6: Properties of Fourier Series

                CSE 219: Signals and Linear Systems

                                   Anik Saha
                 Adjunct Lecturer, Department of CSE, BUET
Properties of Fourier Series

What happens to the coefficients when we play with the signal?
But why will we be learning these properties?

                               x (t)  ak

                          Finding ak directly - needs an integral.
               Properties let us reuse a Fourier series we already know.

                                known signal = related signal

                     Shift it, scale it, add it, differentiate it . . . and
           simply transfer the coefficients without starting from scratch.
Under the hood: every signal is a stack of simple waves

                ak ejk0t

x (t) =

          k =-

Fourier coordinates ak

                              k

-3 -2 -1  0     1       2  3

When we perform any operation on x (t), we are really
 operating on all these simple little waves underneath.
Linearity
Linearity: adding signals simply adds their ingredients

          x (t)                                           y (t)

  x (t) = ak ejk0t                                y (t) = bk ejk0t

                  k                                               k
               ak
                                                                       bk
                                             k
-2 -1 0 1 2                                                                                  k
                                                -2 -1 0 1 2

If they have the same period T , their Fourier axes line up exactly.
Same frequency meets same frequency

x (t) + y (t) = ak ejk0t + bk ejk0t

k           k

      = (ak + bk )ejk0t

              k

new coefficients: ak + bk

                                     k

-2 -1 0  1  2
Linearity of Fourier series

                                 x (t)  ak , y (t)  bk .

                x (t) + y (t)  ak + bk.

                    mix in time  mix the Fourier coefficients
Time Shifting
Time shift: what happens if the signal is delayed?

                                               Goal

                               x (t)  ak
                             x (t - t0)  ?

               Think: if we delay a signal, does its frequency change?
Simple! Just shift every simple wave underneath

              

   x (t) =          ak ejk0t

              k =-

              

x (t - t0) =        ak ejk0(t-t0)

              k =-

     ak e-jk0t0 ejk0t

=

   k=- new coefficient
Time-shifting property

                               x (t)  ak
                     x (t - t0)  ak e-jk0t0

                 A delay in time becomes a phase shift in frequency.
Multiplying by ej means rotating

                                                   Im

                                                     ze j 
                                                                  +

                                                                z
                                                                                               Re

               Multiplication by ej keeps the radius of rotation same,
                         but adds a phase-shift of  to the angle.
So what does the delay factor do?

                            ak e-jk0t0

Magnitude                               Phase

        e-jk0t0 = 1         e-jk0t0 = -k0t0
coefficient size unchanged  only phase changes

Higher-frequency components rotate more . . .
         because their frequency is k0.
Shift in time  Rotation in frequency
Problem: shift the signal, update the coefficients

                                             Suppose
                                       x (t)  ak.
                           Find the Fourier series coefficients of
                                        y (t) = x (t - 3)

                                         in terms of ak.
Answer: delay becomes a phase factor

                             Use the time-shifting property

                     x (t - t0)  ak e-jk0t0

                    For y (t) = x (t - 3), we have t0 = 3. Therefore,
                                p(t) = x (t - 3)  ak e-j3k0

                The magnitudes stay the same; only the phases rotate.
Time Reversal
Time reversal: playing the signal backward

                                               Goal

                               x (t)  ak
                               x (-t)  ?

              Time reversal flips every simple rotating wave underneath.
Let's reverse each Fourier ingredient

                   

          x (t) =        ak ejk0t

                   k =-

                               

x (-t) =        ak ejk0(-t) =          ak ej(-k0)t

          k =-                 k =-

The term that used to live at +k0 now lives at -k0.

                         x (-t)  a-k
Visual intuition: the direction of rotation simply flips!

Original wave     After t  -t

    e jk 0 t      e -jk 0 t

counterclockwise  clockwise

Imagine playing a video of the rotation backward in time.
                     +k0 becomes -k0.
Time reversal property

                               x (t)  ak
                          x (-t)  a-k

             Time reversal in time becomes index reversal in frequency.
Reversal in time  Reversal in frequency
A Problem on everything so far!

                                             Suppose
                         x (t)  ak, y (t)  bk.

                           Find the Fourier series coefficients of
                                      x (4 - t) + y (t - 3)
                                    in terms of ak and bk.
Answer: First part  Shift then Reverse

           x (t)  ak

By time shifting, x (t + 4)  ak ej4k0.

Now, by reversal on t, x (-t + 4)  a-k e-j4k0.

x (4 - t)    a-k e-j4k0 .
Answer: now add the second part

                                            y (t)  bk
                         By time shifting, y (t - 3)  ak e-j3k0.

                                   Therefore,
         x (4 - t) + y (t - 3)  a-k e-j4k0 + bk e-j3k0
Time Scaling
Time scaling: here we change the frequencies themselves

Goal

x (t)  ak ,         2
             0 = T

                       x (t)  ?

Time compression makes every hidden rotating wave rotate faster.
Let's scale every Fourier ingredient

                  

         x (t) =        ak ejk0t

                  k =-

                                      

x (t) =        ak ejk0(t) =             ak ejk(0)t .

         k =-                k =-

               The coefficients are still ak,
but the new fundamental frequency is 0 = 0.
Two views: coefficient index vs actual frequency

       Against index k             Against frequency 

               bk = ak                k0 - k0
The coefficient attached to the  The spectral lines move far-
k-th harmonic stays the same.
                                   ther apart when  > 1.

Time scaling is special: it changes the fundamental frequency itself.
Time-scaling property

                     x (t)  ak with fundamental frequency 0

            x (t)  ak with new fundamental frequency 0
  The coefficient sequence does not change, but the frequency ruler changes.
Practice: combine shift, reversal, and scaling

                                    Let, x (t)  ak
                              with fundamental frequency 0.
      Find the Fourier series coefficients of p(t) = x (4 - 3t) in terms of ak.

                                         Think in order:
                  x (t) - x (t + 4) - x (4 - t) - x (4 - 3t).
Answer: first shift, then reverse, then scale

                                          First shift left by 4:
                                     x (t + 4)  ak ej4k0 .

                                              Then reverse:
                                   x (4 - t)  a-k e-j4k0 .

                                        Finally scale time by 3:
                       x (4 - 3t)  a-k e-j4k0. (Yes, no change!)

                The new fundamental frequency becomes 0 = 30.
Differentiation
Simple, every little wave gets differentiated!

                 

       x (t) =         ak ejk0t

                 k =-

    d                      d
       x (t) =             dt
                       ak      e  jk  0  t
    dt
                 k =-

d   e  jk  0  t  =     jk 0ejk0t
dt

d
   x (t)               (jk0) × ak
dt
But why does the multiplier look like jk0?

                                                                       velocity

                                                                                 position

                                             radius = |ak |
                                          speed = |k0| |ak |

                                Differentiation gives velocity.
          For circular motion, speed is r . Here  = k0 and r = |ak|.
Well! But where does the j come from?

                                                   velocity = (jk0) × ak ejk0t

                                                                           position = ak ejk0t

                                         radius = |ak |
                                      speed = |k0| |ak |

           We need to think in vectors, and therefore, direction matters!
      Velocity is tangent to position, and multiplying by j does exactly that!
Problem: combine properties with differentiation

                            x (t)  ak

                    with fundamental frequency 0.

Find  the  Fourier  series  coefficients  of  p (t )  =  d   x  (4  -  3t )  in  terms  of  ak .
                                                         dt

           Use the result from the previous practice:

           x (4 - 3t)  a-k e-j4k0,                              0 = 30.
Answer: differentiate using the current 0

x (4 - 3t)  a-k e-j4k0 ,              0 = 30.
                  Now differentiate:

d                jk0 a-k e-j4k0 .
   x (4 - 3t)

dt

Since 0 = 30,

p(t)  j 3k0 a-k e-j4k0
Let's draw derivatives of signals!

                  For ordinary smooth parts, derivative means slope.
           At a jump, however, the derivative contains an impulse.

                        jump of height A at t = t0 = A (t - t0)

                              So the derivative has two parts:
                     slope between jumps + impulses at jumps.
Practice: sketch the derivative

         x (t)

         1

···                                       ···  t

-2   -1      0  1                2  3  4

         -1

       d
Find x (t). Remember to include impulses at jumps.

      dt
Answer: slopes plus impulses

         d   x  (t  )
         dt

     2   2             2          2

···                                      ···

                                              t

-2   -1      0         1      2   3  4

-1       -1-1                 -1     -1

Flat part  slope 0 (blue). Slanted part  slope -1 (orange).
       Each jump  an impulse equal to its jump height.
A little detour: impulse as a value-picker

    Let's sum up the product of an arbitrary signal x [n] and an impulse

                                                               

                                                   x [n][n - a]

                                                           n=-

      [n - a] is zero everywhere except at n = a. So only one term survives.

                                                         

                                               x [n][n - a] = x [a]

                                                     n=-
Continuous-time works the same way

                                                             

                                                x (t)(t - a) dt

                                                            -
                                                                                (t - a)

                                                  x (t)

                                                                                                               t
                                                                                     a

                                                       

                                           x (t)(t - a) dt = x (a)

                                                     -
A giraffe only feels the height at the exact point it stands!
A giraffe only feels the height at the exact point it stands!
One caution: the impulse must be inside the interval

                      

R                     x (a), L < a < R,

   x (t)(t - a) dt =

L                     0, a / [L, R].

                         The impulse extracts x (a)
but only if the integration window actually sees the impulse.
Practice: use the sifting property

     Let x (t) = et . Find:

          

     (a)       x (t)(t) dt

          -

             

     (b)       x (t)(t) dt

          1

     5

(c)      x (t) [(t + 1) + 2(t - 2)] dt

     -5
Answer: each impulse picks one value

        et (t) dt = e0 = 1.

(a)

     -

            et (t) dt = 0,

(b)

       1

because the impulse at t = 0 is outside the interval.

     (c) e-1 + 2e2.
Problem: Let's find the Fourier series of an impulse train

                   

          x (t) =       (t - mT )

                   m=-

                        T

···                                    ···

                                            t

     -2T  -T       0       T       2T  3T

Find the complex exponential Fourier series coefficients ak.
Choose one period that contains exactly one impulse

Choose the period

          T         T
       - <t< .
          2         2

              (t )

-T /2        0                       t
                       T /2

       1   T /2
ak = T
                (t)e-jk0t dt.

          -T /2
Now let's use sifting to get the coefficients

       1   T /2
ak = T
                (t)e-jk0t dt

          -T /2

By sifting, the impulse at t = 0 picks the value of e-jk0t at t = 0.

ak  =     1  e -jk 0 ·0  =  1  .
          T                 T

Every Fourier coefficient has the same value:

       1     k = 0, ±1, ±2, . . .
ak = T ,
Frequency-domain picture

                                          1

     x (t) =       (t - mT )           ak = T .

              m=-

                             ak

···                       1                  ···

                          T

                                                  k

-4 -3 -2 -1 0                    1  2  3     4

             The coefficient sequence is flat.
As a line spectrum in , these lines sit at  = k0.
A train remains a train!
Problem: differentiate a periodic rectangular pulse

x (t) = 1, |t| < T1,            x (t + T ) = x (t).
           0, T1 < |t| < T /2,
                                                  ···
                  x (t)
                                                                     t
                  1                          T

···               -T1 0 T1

              -T

                                                                       d
Differentiate x (t), find the Fourier series coefficients of x (t),

                                                                      dt
            and match with the differentiation property.
Known Fourier series of the original signal

                         From previous slides, for the rectangular pulse,
                                           x (t)  ak .

       a0           =  2T1
                        T

ak  =  sin(k0T1) ,     k = 0,         2
            k                  0 = T .
What does the derivative look like?

       +1                         d            +1             ···
                                     x (t)             T
···                                                                    t
                                 dt
              -T           +1                             -1

                       -1  -T1 0 T1
                                           -1

Rising edge gives +. Falling edge gives -.
Write the derivative using impulses

     In one period,

   d
   dt x (t) = (t + T1) - (t - T1).

         For the periodic signal,

d  

dt x (t) = m=- [(t + T1 - mT ) - (t - T1 - mT )] .

Now find its Fourier coefficients directly using sifting.
Let's first find the coefficients directly

Let  the  coefficients      d         be    bk .
                        of     x (t)              Then
                            dt

       1   T /2
bk = T
                [(t + T1) - (t - T1)] e-jk0t dt.

          -T /2

                    Using sifting,

                 1  ejk0T1 - e-jk0T1
          bk = T

              2j
          = T sin(k0T1) .
Now match with the differentiation property

                                 d
Differentiation property says, x (t)           jk0ak .
                                     dt

         For k = 0,   ak  =      sin(k0T1) .
                                      k

jk 0 ak  =  jk  0  sin(k 0 T1 )     =  j  0  sin(k 0 T1 ).
                        k                 

                2                       2j
Since 0  =         ,  jk0ak = T sin(k0T1) .
                T
Perfect match

                                        Direct calculation gave
                             2j
                      bk = T sin(k0T1). (this already also gives b0 = 0)

                                    Differentiation property gave
                                                    2j

                                       jk0ak = T sin(k0T1).

                           bk = (jk0) × ak
Integration
Integration: reverse of differentiation

x (t)  ak

d                                        jk0ak .
Differentiation says, x (t)    
                           dt

So integration should divide by the same factor:

x (t) dt  ak ,                           k = 0.
                      jk 0
One important warning: the constant term

Integration cannot recover the constant term.

                           Why?

d                 d
    (x (t) + C ) = x (t).
dt                dt

So after integrating, the a0 term must be determined separately.

    bk  =   ak ,  k = 0
           jk 0
Problem: use differentiation first, then integrate back

x (t) = t, 0  t < 1, x (t + 1) = x (t).

         x (t)

         1

···                      ···

                                                 t

-2   -1     0   1  2  3  4

Find the Fourier series coefficients of x (t)
by first finding the series for the derivative.
Derivative of the sawtooth

Between jumps, the slope is 1. At each integer, the signal jumps down by 1.

        d                       

    y (t) = x (t) = 1 -              (t - m).
        dt
                                m=-

        y (t)

        1

                                                   t

-2  -1      0               1   2    3         4

-1  -1     -1               -1  -1   -1        -1
Fourier coefficients of the derivative

             

y (t) = 1 -       (t - m).

             m=-

The constant part 1 has coefficients

                          

                      1, k = 0,
       1 

                      0, k = 0.
Fourier coefficients of the derivative

             

y (t) = 1 -       (t - m).

             m=-

The impulse train part has coefficients 1 for all k.  (  1  =  1  = 1)
                                                         T     1

                                                        

                                       0, k = 0,
Therefore, y (t)  bk = -1, k = 0.
Integrate back to get the coefficients of x (t)

    d                     bk = jk0ak .
y (t) = x (t)     =
         dt

    So, for k = 0,

       ak      =   bk .
                  jk 0

Here bk = -1 and 0 = 2, so

ak  =  -1 j               k = 0.
               =       ,
       j 2k       2k
Do not forget a0

    Integration did not determine a0.
Let's just find it from the average value:

                                     1  1

                            a0 =        t dt = .
                                                 2
                                  0

                  a0  =  1                 j
                          ,       ak = 2k , k = 0.
                         2
Multiplication
New goal: what about multiplying two signals?

                                                 So far, if
                                   x (t)  ak , y (t)  bk ,

                                         then linearity gives us
                                   x (t) + y (t)  ak + bk .

                              But what about multiplication?
                                      x (t)y (t)  ?
Simple! Let's multiply the two Fourier series

                                  

x (t) =       apejp0t ,  y (t) =       bqejq0t .

         p=-                      q=-

                                               

x (t)y (t) =        apejp0t         bqejq0t  .

               p=-             q=-

We use p and q because the two sums need separate indices.
This is nothing but polynomial multiplication!

Let, z = ej0t . Then,

ejp0t = z p,     ejq0t = z q.

x (t) = apzp,    y (t) = bqzq.

              p                q

It becomes becomes multiplying two coefficient-polynomials in z!
Which terms create the k-th frequency?

When we multiply one term from x (t) and one term from y (t),
                  apejp0t · bqejq0t = apbqej(p+q)0t .

           To contribute to the k-th harmonic, we need

      p + q = k.

So q = k - p, and the k-th coefficient becomes

ck =              ap  bk  -p            .
      p=-
Multiplication property: Convolution Returns, Again!!!

x (t)  ak , y (t)  bk ,

x (t)y (t)  ck = (a  b)k

      

ck =       ap bk -p .

      p=-

Multiplication in time becomes convolution in frequency.
Practice: square a simple signal

     Let, x (t) = 1 + cos(0t).
Its nonzero Fourier coefficients are

a-1  =  1   a0 = 1,               a1  =  1
         .                                ,
        2                                2

Find the Fourier series coefficients of
              p(t) = x 2(t).
Answer: convolve the coefficient sequence with itself

Since, p(t) = x (t)x (t),

                      ck = (a  a)k = apak-p.

                                                            p

Only a-1, a0, a1 are nonzero. So we compute the convolution:

k -2 -1 0 1 2

ck  1  1  3  1  1
    4     2     4
Let's check using ordinary trigonometry

               x 2(t) = (1 + cos(0t))2

= 1 + 2 cos(0t) + cos2(0t)

            3             1
= 2 + 2 cos(0t) + 2 cos(20t).

Therefore,     c0  =  3   c±1 = 1,       c±2  =  1
                       ,                          .
                      2                          4
Thank you!


# Anik Sir/Lecture-7-Fourier-Transform.pdf

Lecture 7: Fourier Transform

     CSE 219: Signals and Linear Systems

                         Anik Saha
           Lecturer, Department of CSE, BUET
Fourier Transform: to  and beyond

       Looking inside any function. Yes, not just periodic ones!
Aperiodic functions crying in the background. . .
Fourier Transform

                    When the period goes to infinity!

                       Fourier series decomposes periodic signals.
       Fourier transform lets us do something similar for aperiodic signals.
Fourier series had one big condition

Fourier Series         But real signals
                         often do not

x (t + T ) = x (t)     no fixed period

                    t

keeps repeating                          t

                       one-time event

Can we still describe a non-repeating signal using frequencies?
Let's cheat first: repeat one lonely pulse

Start with one finite-duration signal x (t)

                       

             xT (t) =       x (t - mT )

                       m=-

                            T

···                    0                        ···

         -T                                               t
                                            T

Now it is periodic, so Fourier series works.
Now stretch the period

  Small T                  Large T

copies are close        t                    t

                           copies move away

As T  , the repeated signal
starts looking like one isolated signal.
What happens in frequency?

                            2   = 0.
                     0 = T ,

Small T , large                Large T , small 

                                                     

few frequency lines            many frequency lines

Increasing T makes the allowed frequencies closer and closer.
Fourier-series coefficients of the repeated signal

The periodic signal has Fourier series

          

xT (t) =        ak ejk0t

          k =-

       1  one period xT (t )e-jk0t dt
ak = T

This is still the same Fourier-series coefficient formula.
Choose one period that contains the pulse

                                x (t)                    t
-T /2                                  T /2

       1   T /2
ak = T
                xT (t)e-jk0t dt

          -T /2

Inside this period, xT (t) is just the isolated pulse x (t).

          1
A smooth spectrum is hiding behind the stems

Look at the integral part

       1   
ak = T
              x (t)e-jk0t dt

          -

          depends on k0

             Let
X (j) =  x (t)e-jt dt

                  -
So the stems are samples of a smooth curve

                                             Tak = X (jk0)

                                                                      X (j)

                                                                  smooth envelope

                                                                                                                              

                Fourier-series samples

              As T increases, the sample locations k0 become closer.
But why do raw coefficients shrink?

       1
ak = T X (jk0)

      Since
                2

 = 0 = T ,
     we have

1  =  
          .
T 2
Think of it like frequency-density

stem amount  spread over a bin

                                                                                                  
                                                 

  When   0, the bins become thinner and thinner,
and the discrete spectrum becomes a continuous spectrum.
The Fourier-series sum becomes an integral

Start from Fourier-series synthesis

                

xT (t) =            ak ejk0t

              k =-

         Use
       
ak = 2 X (jk0).

           1    X (jk0)ejk0t 
xT (t) = 2
Let T  

                     2
         T        =  0 =  = T  0

       k 0           becomes

becomes a con-       jt
tinuous variable

        

                  1
The Fourier transform pair

Analysis                    Synthesis

X (j) =  x (t)e-jt dt x (t) = 1  X (j)ejt d 
-                           2 -

x (t) - X (j)               X (j) - x (t)

Fourier transform is Fourier series after
the frequency lines become continuous.
The whole story in one picture

   Fourier Series     Increase T         Fourier Transform

   periodic signal      =  2    0          aperiodic signal
discrete frequencies       T            continuous spectrum
                      stems get closer

       Fourier transform is not a totally new idea.
It is the continuous-frequency version of Fourier series.
Let's keep rotating and oscillating random things. . . !
Injecting oscillation into a signal

                   x (t) - x (t) cos(0t)

Envelope x (t)     Oscillation             Oscillating
                                            envelope
        x (t)         cos(0 t )
                                            x (t) cos(0t)
                t
                                     t
                                                                               t

We keep the shape of x (t) as an en-
velope, but put oscillation inside it.
This happens in real systems too

                                   A damped oscillation

                                  x (t)

                                                                                  decay envelope
                                                                                                                   t

                                 oscillation + decay

                     Examples: damped pendulum, vibrating string
                         with loss, ringing circuits, fading echoes.
So what transform should we expect?

                                         x (t)  X (j).

                     What is the Fourier transform of
                                 x (t) cos(0t)?

                            Let's first solve the cleaner version:
                                            x (t)ej0t .
Multiplying by ej0t shifts every frequency

                         A frequency component inside x (t) looks like
                                                    ejt .

                                      After multiplying by ej0t ,
                                        ejt · ej0t = ej(+0)t .

                Every component at  moves to  + 0.
The spectrum slides to the right

Before                            After multiplying by ej0t

X (j)     =                       X (j( - 0))

                                                       
                                  0

To move the spectrum right by 0, we write X (j( - 0)).
Frequency-shifting property

                                                      If
                                         x (t)  X (j),

                                                    then

                     x (t)ej0t  X j( - 0)

            Multiplication by a complex exponential shifts the spectrum.
Cosine is two rotating exponentials

               1  ej0t + e-j0t
cos(0t) = 2

                  So

x (t) cos(0t)  =  1 x (t)ej0t  +     1 x (t)e-j0t .
                  2                  2

A cosine creates two shifted copies of the spectrum.
Cosine modulation creates two spectral copies

left copy          original X (j)  right copy

               -0                                                 
                                   0

                   1   j( - 0)                 1
x (t) cos(0t)       X              +X             j( + 0)
                   2                  2
What did oscillation do?

         In time:                In frequency:
 x (t)  x (t) cos(0t)
We injected oscillation.  X (j)  two shifted copies

                                The spectrum
                                moves to ±0.
A very common transform: the rectangle

                  T     T

         1, - < t < ,
x (t) =           2     2

         0, otherwise.

           x (t)
         width T

           1

-T /2                                            t
                     T /2

This transform appears everywhere, let's keep it in our toolbox :D
Fourier transform of the rectangle

Since x (t) = 1 only from -T /2 to T /2,

                    T /2   e-jt dt.

         X (j) =

                    -T /2

X (j) =  e-jt T /2   =     ejT /2 - e-jT /2  .

         -j   -T /2                 j

                    2 sin(T /2)
         X (j) =

                           
Wider rectangle, narrower spectrum

                      T    X (j) =  2 sin(T /2)  .
x (t) = 1, |t| <
                                    
                       2

Time domain                  Frequency domain

      large T                 narrow main lobe

                          t                         
Practice: two centered rectangles

                                      

          1, -1 < t < 1,            1, -3 < t < 3,
x1(t) = 0, otherwise.     x2(t) = 0, otherwise.

X1(j) =?                           X2(j) =?

                          Use

width T = X (j) =                  2 sin(T /2)  .

                                   
Answer: just plug in the width

For -1 < t < 1, the width is T = 2:

X1(j) =                         2 sin()
                                      .
                                

For -3 < t < 3, the width is T = 6:

X2(j) =  2 sin(3)
                                      .
                                

The same rectangle formula works once we identify the width.
What if the rectangle is shifted?

           1, 4 < t < 10,
x (t) =

           0, otherwise.

                                                  wciedntther6
1

                                                                    t

4                                  7                            10

This is a width-6 centered rectangle shifted right by 7.
Answer: rectangle formula plus time shift

A width-6 rectangle centered at zero has transform

R(j) =  2 sin(3)  .

        

Our signal is

          x (t) = r (t - 7).
       Using time shifting,
r (t - t0)  e-jt0R(j).
A Lego block signal

                                    1 < t < 2,
                                    2 < t < 3,
                              1,    3 < t < 4,
                                    otherwise.
                               
                               
                              1.5,
                     x (t) =
                              1,
                               
                               
                               
                              0,

  x (t)              looks complicated?
1.5

  1

                                                t

                     1  2           3  4
Decompose the Lego block

x (t) = height 1 rectangle from 1 to 4 + height 0.5 rectangle from 2 to 3 .

wide block                         small top block

            width 1, center 2.5

            width 3, center 2.5

                                   t

            1             2  3  4
Fourier transform of the Lego block

                                Wide block:
         width 3, center 2.5 = e-j2.5 2 sin(1.5) .

                                                             
                                 Top block:
height 0.5, width 1, center 2.5 = 0.5e-j2.5 2 sin(0.5) .

                                                                       

X  (j )  =  e -j 2.5  2  sin(1.5)    +  sin(0.5) 

                                                        

                                        
Now lock a cosine inside the rectangle

Let r (t) be the rectangle from -T /2 to T /2.

x (t) = r (t) cos(0t)

windowed cosine

-T /2                        t
       T /2

This is just modulation of a rectangle.
A windowed cosine creates two sinc-shaped copies

copy  copy

-0                                
      0

A cosine inside a rectangle has spectrum
 centered around ±0, not around zero.
Fourier transform of a spike

     x (t) = (t)

                              x (t)

                                 area = 1

···                                        ···  t

                              0

What does this single spike look like in the frequency domain?
Simple, let's use the sifting property!

For x (t) = (t),

            (t)e-jt dt.

X (j) =

         -

Now the impulse simply samples the background function at t = 0:

 

    (t)f (t) dt = f (0).

-

X (j) = e-j·0 = 1.
So the spectrum is completely flat

(t)  1

Time domain                                Frequency domain

           (t )                                            X (j)

              1                            ···  1                 ···

                                        t                                      
            0                                      0

A very narrow spike in time needs all frequencies equally.
Small bonus: what if the spike is shifted?

Let, x (t) = (t - t0).

Then, X (j) =     (t  -  t0)e-jt dt.
               -

Using sifting, the impulse samples the exponential at t = t0:

X (j) = e-jt0 .

(t - t0)  e-jt0
Applications

Where Fourier transform quietly appears
Audio Denoising

     Remove the unwanted frequencies
Audio denoising: keep the voice, reduce the noise

             =t                                    t

noisy audio      cleaner audio

Fourier transform lets us see which frequen-
cies are voice-like and which are noise-like.
Image Denoising

 Clean an image by editing its frequencies
Image denoising: noise often hides in high frequencies

Image  Frequency view  Filtered image

       A blurry-but-clean image is often
       better than a sharp-but-noisy one.
JPEG Compression

      Throw away what the eye barely notices
JPEG compression: not all frequencies are equally important

image block  frequency block  compressed block

small high-frequency coefficients are rounded away

Fourier-like ideas help images become
smaller without looking very different.
         MRI

The scanner collects frequency-domain data first
MRI: the picture is reconstructed from frequency samples

Measured data                Reconstructed image

               =

k -space       image

MRI is a beautiful real-life case where fre-
 quency domain comes before the image.
Music Recognition

               Fingerprints in frequency
Music recognition: a song can be identified from frequency
peaks

frequency                 another fingerprint

             fingerprint

                                                                                 time

Even a short audio clip can reveal a
unique pattern of strong frequencies.
Vibration Diagnosis

           Machines complain in frequencies
Vibration diagnosis: a faulty machine changes its spectrum

Healthy    Faulty

                                          

A bearing crack or loose part may be
easier to see in frequency than in time.
ECG Filtering

Rescue the heartbeat from interference
ECG filtering: remove hum without destroying the heartbeat

heartbeat

           power-line hum

                                                  t

Fourier transform helps design filters that
 remove unwanted frequencies carefully.
Thank you!
Thank youuu! Until we meet again. . .


# Ashraf Sir/Lecture 1 - DTFT and DFT.pdf

DTFT and DFT

Signals and Linear Systems

Ashrafur Rahman
Lecturer, CSE, BUET

ashrafur@cse.buet.ac.bd
Last Time: Four Transforms, One Square

· Last class ended on a promise: one structural rule generates every Fourier-type transform.
· We already know the left column -- the CTFS and the CTFT -- from continuous-time analysis.
· Today we derive the right column: what happens to Fourier's idea when time arrives in samples.

           time is continuous           time is discrete

periodic   Fourier Series (CTFS)            DFS / DFT
                   known                today, Part I & III

aperiodic  Fourier Transform (CTFT)          DTFT
                     known              today, Part II

                                                                                                  1
Outline

           · Part I -- From Fourier Series to the DFT: sample a periodic signal; the Fourier integral becomes a sum; the
              Discrete Fourier Series (DFS); the DFT and its inverse.
                     · Reading the bins: where the negative frequencies live.

           · Part II -- The Discrete-Time Fourier Transform: sample an aperiodic signal; the DTFT, its 2-periodicity,
              and its inverse.

           · Part III -- The DFT Through the DTFT Lens: the DFT as N evenly spaced samples of the DTFT; zero-padding;
              a worked example; bins in hertz.

                                                                                                                                                                                                                           2
From Fourier Series to the DFT
Recap of the CTFS

· Let's start with a continuous-time periodic

signal x(t) with period T0:                    x(t)

                                      2
x(t + T0) = x(t),            0           .
                                      T0             T0  T0

· We have learnt the Continuous-Time Fourier
  Series (CTFS) representation:

CTFS Pair                                                    t

                                                                            3

x(t) =                  ck ej k0 t

                   k=-

        1              x(t)e-j k0 t dt
ck = T0
                     T0
Seeing the Fourier Series: Wind One Period

· Multiply x(t) by e-jk0t: each value becomes a radius and k0t an angle, so the graph is wound around

the origin, k turns per period.       The coefficient  ck  =   1  T0 x(t) e-jk0tdt is the center of mass of the
wound curve.                                                  T0

x(t) = 1 + 0.8 cos 0t + 0.5 cos 20t,  k = 1: the loop closes, centroid = c1 = 0.4 k = 3: the mass cancels, centroid = c3 = 0
                     one period

· One period is enough: after T0 the angle has advanced by 2k, so every later period retraces the same
  loop. Only the rates k0 close it -- hence a line spectrum.

 Interactive: wind one period of this signal; step the rate through its harmonics Picture after 3Blue1Brown, But what is the Fourier Transform? (2018)  4
Uniform Sampling of a Periodic Signal

sWigenalrex[inn]t.erested in a representation for discrete signals. We can sample x(t) to get a discrete

· Sample x(t) uniformly with sampling                            x[n]                  N samples
  period Ts.                                                                N samples

· Assume T0 is captured by N samples:

                T0 = N Ts (N  Z+).

· The purely discrete sequence x[n] is                                                                    n

defined as:                                                      Ts

x[n]  x(nTs), n  Z.

· Thus x[n] is inherently N -periodic:

             x[n + N ] = x[n].                                   T0 = N Ts

 Interactive: sample this waveform: slide N and watch Ts shrink                                              5
Sampling as an Impulse Train

· We can represent the sampled signal mathematically using an impulse train (aka Dirac comb).
· Multiplying the continuous signal x(t) with the impulse train p(t) gives us the sampled signal xp(t).
· Each sample x[n] is weighted by a Dirac delta function at time nTs.

p(t)                                                        xp(t)

                                                         t                                                            t
        Ts                                                         Sampled signal xp(t) = x(t)p(t).
      Impulse train p(t) =  (t - nTs).

                                                                    

      xp(t) =                      x(nTs) (t - nTs) =                 x[n] (t - nTs).

                              n=-                           n=-

                                                                                                                         6
The Integral Becomes a Sum

    · The sampled signal xp(t) is still T0-periodic, so it has a CTFS. Let ck be its coefficients:

                                                                  1             xp(t) e-jk0t dt.
                                                          ck = T0
                                                                             T0

    · Substitute xp(t) =                       x[n](t     -  nTs    );  the  impulses       sift  the   integral:
                                    n=-
                                                                                      
                                              t0+T0   x[n](t - nTs) e-jk0t dt
                                     1
                             ck = T0       t0           n=-

                                =   1 N-1      x[n]    t0 +T0       (t - nTs)e-jk0t dt               =      1   N -1
                                                      t0                                                    T0
                                    T0 n=0                                                                            x[n] e-jk0nTs

                                                                                                                n=0

    ·  Since 0Ts      =  2      Ts  =   2  ,  we  arrive  at  a   finite  sum:
                         T0             N

                                                                        1    N -1                2
                                                                        T0                       N
                                                              ck  =                x[n]  e-j         kn  .

                                                                             n=0

We  can  take  t0  =  -  Ts  ,  so  (t  -  nTs )  is  non-zero  in  [t0, t0  +  T0 ]  only  for   n  =  0, 1, 2, . . . , N  -  1.
                          2

                                                                                                                                     7
Only N Distinct Coefficients

· Examine the exponent in ck:                                        |ck |

         1   N -1                      2                                    N -periodic       same N values,
         T0                            N                                                       over and over
ck+N  =                       x[n]e-j     (k+N  )n

             n=0

      = ck e-j2n = ck

             =1

· The frequency coefficients are N -periodic:
  sampling in time made the spectrum
  periodic!

· Only N unique frequency values exist
  before the spectrum repeats.

· We conventionally keep the window                                                                           k
  k = 0, 1, . . . , N - 1.
                                                              -N  -  N      N              N  3N  2N
                                                                     2
                                                                            2                 2

 Interactive: sample a period, watch ak repeat with period N                the N we keep

                                                                                                                 8
Reading the Bins: Where the Negative Frequencies Went

· The natural spectrum is centered                                                   |ck |
  at k = 0: low frequencies in the
  middle, negative k on the left.                 negative                                     positive

· Periodicity moves each negative                                                                                      k
  coefficient into the window                                                                            N
  0, . . . , N - 1:                                                                                       2

                 c-k = cN-k.                   -  N
· The negative side is not lost -- it             2

  folds onto the upper bins.            |ck |

 How to read N bins

Bins 0     N  :  positive frequencies,
           2
low  high.    Bins  N   N : nega-
                    2
tive frequencies, high  low. A real

lowpass signal peaks at k = 0 and                                                                                      k

near k  =  N , and dips at k  =  N  .                                                       N                       N
                                 2
                                                                                            2

                                                       positive: low  high                     negative: high  low

 Interactive: explore the bins on a live DFT: hover, click, or draw your own period                                       9
Can CTFS Synthesis Give Us Back x[n]? No.

· We cannot simply use the CTFS synthesis equation to recover our discrete signal:

                                                                                 

                                                                   ckejk0t = xp(t)

                                                                             k=-

· It rebuilds the continuous-time impulse train xp(t) -- not the sequence x[n] we want -- and it spends
  infinitely many terms repeating the same N coefficient values.

xp(t)                                         x[n]

                                           t                                                             n

What CTFS synthesis rebuilds: impulses.             What we want: the sequence itself. 

· But there is a familiar pattern: analysis uses e-j···, synthesis uses e+j···. Let's build a discrete synthesis
  that uses only the N unique coefficients.

                                                                                                                  10
The Inverse Trick (1/2): Orthogonality

· From the analysis sum, the N unique coefficients are (writing T0ck to clear the scaling):

                                          N -1                2
                                                              N
                                T0 ck =           x[m]   e-j      km  ,   k = 0, 1, . . . , N - 1.

                                          m=0

·  Multiply  both  sides  by  e+j  2  kn  and  sum   over   the  N  unique k:
                                   N

                              N -1                2         N -1    N -1            2             2
                                                  N                                 N             N
                                    (T0 ck )  ej     kn  =                x[m]e-j      km     ej     kn

                              k=0                           k=0     m=0

                                                            N -1          N -1      2
                                                                                    N
                                                         = x[m]                 ej     k(n-m)

                                                            m=0           k=0

· Evaluate the inner summation using the geometric series sum formula. For n = m:

                          N -1     ej  2  (n-m)      k 1 - ej2(n-m)          =         1-1           =0
                          k=0          N             =
                                                                   2                       2
                                                         1  -  ej  N  (n-m)     1   -  ej  N  (n-m)

                                                                                                         11
The Inverse Trick (2/2): The Discrete Inverse

· And for n = m, the summation simply evaluates to:

      N -1                                              N -1      2                N  n=m
                                                                  N
                    e0 = N =                                  ej     k(n-m)  =

      k=0                                               k=0                        0 n=m

· All terms in the outer sum vanish except m = n:

N -1                2                                                           1  N -1                  2
                    N                                                           N                        N
      (T0 ck )  ej     kn  =                   x[n]  ·  N     =      x[n]    =           (T0  ck  )  ej     kn  .

k=0                                                                                k=0

· A finite sum recovers the samples exactly -- no impulses, no infinite series.

· Notice: both directions only ever touch the N numbers T0ck. That combination is the natural
  discrete-frequency object -- it deserves its own name.

                                                                                                                   12
The Discrete Fourier Series (DFS)

· Forget the continuous signal for a moment: let x~[n] be any N -periodic sequence. The same finite sums
  form a self-contained series representation:

Discrete Fourier Series (DFS) Pair

                                   1  N -1              2                                         N -1           2
                                   N                    N                                                        N
ak  =                                       x~[n]  e-j                 kn               x~[n] =          ak  ej     kn

                                      n=0                                                         k=0

                                       analysis                                                   synthesis

· It is the exact discrete analogue of the CTFS -- same shape, integral  sum -- and its validity is exactly
  the orthogonality trick from the last two slides:

                                   CTFS (period T0)                                     DFS (period N )

Analysis                           ck  =   1        x(t)    -jk              2   t  dt  ak  =  1  N -1       x~[n]  e-jk  2  n
                                          T0              e                  T0                N  n=0                     N
Synthesis                                     T0
Coefficients                                                                 2
                                   x(t) =               ck               jk  T0  t      x~[n] =   N -1   ak  ejk    2  n
                                              k=-                      e                          k=0               N

                                   infinitely many                                      N unique (ak+N = ak )

 Interactive: the DFS of one period: every k, repeating with period N                                                           13
Seeing the DFS: Wind the N Samples

·  Wind the N    samples      instead   of  the  curve:               point     n  sits  at  radius     x[n],  angle  -   2  kn.       Their center of mass
                                                                                                                          N
                                                                             2
   is  the  DFS  coefficient  ak  =  1      N -1  x[n]                e-j    N  kn:  a   plain  average  --    that   is  why      the  integral     became      a
                                     N      n=0
   sum.

                                                                                                   n=0                n=1                                   n=0

                                                                                     2                                                  6
                                                                                      8                                                  8

                                                                                        n=1

   N = 8 samples of that period                  k  =              1  (  2   per sample):  a1  =  0.4                 k   =  3  (  6   per sample):  a3  =  0
                                                                          8                                                         8

·  Every sample turns  by the same angle            2bNykt;haeftsearmNe              samples the points        repeat, so one           period is still
   enough. And k + N   turns each sample                                             angle mod 2: only         N coefficients           are distinct --
                                                                                                                                                                 as

   derived.

 Interactive: wind its 8 samples; click any bin to wind at that k                                                                                                    14
The Discrete Fourier Transform (DFT)

· For a length-N sequence {x[n]}nN=-01, define the transform as the bare analysis sum (no scale factor). It is
  customary to write it with the twiddle factor

                    WN        e-j  2  ,  WNN = 1 (an N -th root of unity -- powers of WN cycle).
                                   N

   DFT / IDFT Pair

                       N -1                N -1                       2
                                                                      N
           X[k]               x[n] WNkn =        x[n]           e-j      kn   ,                        k = 0, 1, . . . , N - 1
                                                                                                       n = 0, 1, . . . , N - 1
                       n=0                 n=0

                       1      N -1                 1            N -1              2
                       N                           N                              N
           x[n]     =               X[k] WN-kn  =                     X  [k]  ej     kn  ,

                              k=0                               k=0

·  Connection to the DFS: X[k] = N ak -- the DFT of a periodic discrete signal is its DFS, up to the                                 1
                                                                                                                                     N
   convention factor.

·  Connection to the sampled continuous signal:                 ck    =   1      X [k]  --  the  CTFS  coefficients  of  xp(t)  are  the  DFT
                                                                         T0
   values  scaled  by   1  .
                       T0

 Interactive: the N bins of the DFT, with X[k] = N ak on hover                                                                                 15
We Never Needed the Continuous Signal

· Look at the DFT formula again: it consumes only the N numbers x[0], . . . , x[N - 1]. Nothing in it
  remembers Ts or x(t).

· The sampling story was scaffolding: its only job was to show why the Fourier integral became a sum once
  the signal lived on samples.

· Any length-N (or N -periodic) list of numbers -- an audio buffer, a pixel row, a sensor log -- has a
  DFS/DFT, no continuous ancestor required.

x(t)  x(nTs)                                                                                                                              x[n]

      sample                                                                                                                                forget            n
                                                                                                                                          the clock
       t                                                                                                                                             N -1
                                                                                                                                           t

                                                                                                                                      Ts

Scaffolding removed

DFS: a Fourier series whose integral collapsed to a sum. DFT: the DFS, rescaled. That is all they are.

 Interactive: draw the N samples yourself -- no x(t) required                                                                                                    16
Part I in One Picture: N Points  N Coefficients

                                                  N points in Time                              N points in Freq

· We started with a continuous-time periodic                                              DFT   N N -1
  signal x(t).                                                                            IDFT  2

· Sampling it yielded a periodic discrete         · positive frequencies (low  high)
  sequence x[n] with period N .                   · folded negative frequencies (high  low)

· Its frequency representation ck is uniquely
  defined by exactly N contiguous components.

· The DFT transforms exactly N points of x[n]
  into N unique frequency coefficients X[k].

· The IDFT perfectly reconstructs those N points
  in time from these N frequency values.

                                                                                                                  17
The Discrete-Time Fourier Transform
Now Let the Signal Be Aperiodic

Bu·t Ldeot'esscothnissidmeraacnhianpeerryioodniclysiganpapllxy(tto) rpeestrriiocdteidc tsoiganfainlsit?e Winhteartvaifl Tth0e. signal is aperiodic?
   · Uniformly sampling this yields a finite-length sequence x[n] that is nonzero only for 0  n  N - 1.
   · Using the impulse-train representation, the sampled signal is:

                                                                                   N -1

          xp(t) = x(t)p(t) =                   x[n](t - nTs) = x[n](t - nTs)

                                          n=-                                      n=0

x(t)                                x[n]                                              xp(t)

      T0

                                 t                                                 n         t

 Interactive: a finite burst, its samples, and what sampling does to its spectrum                                 18
CTFT of the Samples: The DTFT

· An aperiodic signal calls for the Fourier transform. Take the CTFT of the sampled impulse train:

                                                                       

                               Xp(j) =                                       x[n]e-jnTs

                                                                       n=-

· Now compress the frequency axis by the sampling period, i.e. apply the mapping Ts  .
· Under that relabeling, the same spectrum becomes the Discrete-Time Fourier Transform (DTFT):

Discrete-Time Fourier Transform (DTFT)

                                                                             

                               X(ej )  Xp(j) Ts =                                 x[n]e-j n .

                                                                             n=-

· Hence, the DTFT is the Fourier transform of the sampled signal, with a compressed frequency axis. The
  new  is digital frequency: radians per sample.

· For our length-N capture,                                            N -1

                               X(ej) =                                       x[n]e-j n .

                                                                       n=0

 Interactive: the DTFT of a handful of samples, as a continuous curve                                    19
Aperiodic: Wind the Whole Segment, at Any Rate

           · Take a finite segment of a shifted cosine, x(t) = 1 + cos 6t for 0  t  1.5 s: nothing repeats outside it,
              so the winding runs over the entire segment, and its centroid times the duration is the transform
              X(j) = x(t) e-jtdt. No rate is special, so every  gets its own value: a continuous spectrum.

x(t) = 1 + cos 6t on 0  t  1.5 s: 4.5               = 4 (2 Hz): mostly cancels, centroid   = 6 (3 Hz): a perfect cardioid, centroid
                          cycles                                         0.08j                                0.5 - 0.07j

· At the cosine's own rate every cycle traces the same cardioid r = 1 + cos , and the mass sits to the right
  of the origin. At any other rate the cycles spread around the circle and nearly cancel; the small residue --
  here from 4.5 cycles not closing -- is the continuous skirt of the spectrum.

 Interactive: wind the cosine segment at any rate                                                                                    20
Only N Points to Wind: The DTFT and Digital Frequency

·  Sample the segment, x[n] = x(nTs) with Ts =                            1   s:  the  winding   places  the  points  x[n]  e-jn  on  the
                                                                          24
   same curve, and with no period all of them count, X(ej) = n x[n] e-jn = N ·centroid. Consecutive
   points are turned by the same angle  -- the digital frequency, in radians per sample, equal to physTs.

                                                                                            n=0                                       n=0
                                                                                                                            

                                                                                       n=1                                     n=1

N = 36 samples, 8 per cycle, on the same                  = /6 per sample = 4Ts: centroid                 = /4 per sample = 6Ts: centroid
                         cosine                                                0.09j                                      0.5 - 0.07j

·  3piHlizngbeucpotmheesre6.Tu· r2n14in=g       radians  per  sample, and the 36 points land on just 8 spots of the         cardioid,
                                                 + 2     per  sample places the very same points, so X(ej) must             repeat every
                                           b4y

   2 -- next slide.

 Interactive: wind its 36 samples: 8 per cycle, so 3 Hz is /4 per sample                                                                   21
The DTFT Is 2-Periodic

        Period of the DTFT                                                    one period = 2 (principal interval [-, ])

        Each term repeats every 2 (as                                                   |X (ej )|
        e-j2n = 1), so:

                 X(ej(+2)) = X(ej )

                                                                              high freq          high freq

        How to Read One Period

            · Any 2-wide window holds one full                            -2  -                  low freq                   
              period.                                                                                                    2
                                                                                       negative             
            · A common principal interval is
              [-, ].                                                                             positive wrapped negative

            · [, 2) is the folded copy of [-, 0).

                                                                                                 -2 shift

Before Ts   the axis was physical frequency. Undoing

the  relabel,  [-,   ]     corresponds  to  [-  s   ,  s   ]  with  s  =
                                                 2      2

2    ;  we  revisit  that  view  in  Sampling.
Ts

 Interactive: pulses, decays and tones: their DTFTs over two periods                                                          22
The Inverse DTFT

· Same pattern as Part I: synthesis should use e+jn. But the spectrum is now a continuous function of ,
  so instead of summing over N unique bins we integrate over one 2 period:

                                  1           X(ej ) ejn d.
                       x^[n] 
                                     2 2

· Substitute the analysis sum X(ej) = m x[m]e-jm and swap sum and integral:

                                              1

                       x^[n] =          x[m]  2 2  ej(n-m) d.

                                m=-

· Orthogonality over one period: for integer r = n - m, complete cycles integrate to zero:

                  1                  1  r=0        =         x^[n] = x[n].

                        ejr d =
                  2 -                0 r=0

Inverse DTFT

                                  1     X(ej ) ejn d
                       x[n] =
                                2 2

                                                                                                         23
The DTFT Pair, and the Square So Far

DTFT Pair                                                         continuous t                     discrete n

                                                                                   sample
                                                                                     in t
X(ej) =         x[n] e-jn                   periodic           1   CTFS                            DFS / DFT 
                                                              T0  T0 x(t)e-jk0tdt
           n=-                                         ck  =                               X[k] =  N -1  x[n]WNkn
                                                                                                   n=0

           1    X(ej ) ejn d                                                                       sample in ?
x[n] =                                                                                                   next
           2 2

· x[n] is a continuum superposition of      aperiodic                CTFT          sample          DTFT 
  ejn over one period -- versus the DFS: a             X(j) = x(t)e-jtdt
  finite sum of N of them.                                                         in t    X(ej ) = n x[n]e-jn

                                                                                                                   24
The DFT Through the DTFT Lens
The DFT Samples the DTFT

· Recall the DFT definition -- and just look at it: it is                     |X (ej )|

   the DTFT evaluated at discrete frequencies

     =  2  k.  Nothing    to  derive:                                                       2
        N                                                                                   N

               N -1                                                                                 DFT evaluates N bins

     X[k] =          x[n]  e-j  2  kn               =  X (ej )             .
                                N
                                                                    2
               n=0                                              =   N   k

· So the N -point DFT takes N evenly spaced
  samples over one 2 period of the DTFT.

·  For  even N :  pboinsistikve=fr0e,q.u.e.n, cN2y;    climb  from  dc  to
   the  highest                                        bins
                                                                                                                                         

   kfre=quN2en+cie1s,.. . . , N - 1 hold the folded negative                                                              2

                                                                                         k  =  0, . . . ,  N  k=  N  + 1, . . . , N - 1
                                                                                                           2      2
One transform, two views

           Periodic view: Fourier-series coefficients. Aperiodic view: N samples of the DTFT.
                                                       Same N numbers.

 Interactive: watch the bins sit on the DTFT curve                                                                                         25
Reading DFT Bins, Once More

·  Bin k sits     atht efko=lde2Ndnke; gpaatsivt ek  =  N
   these are                                            2

   frequencies. For N = 8:                                                         |X(ej )|

   k 01 2 3 4 5                      67                    negative                                  positive

   k     0              3     -  3   -               -                                                                   
            4     2      4        4     2               4                                                   

· dc  rising positive  highest ()                                          -
  negative, falling back toward dc.                        |X(ej )|

   How to read N bins

   Bins 0      N  :  positive frequencies, low
               2
    high.      Bins     N    N : negative fre-
                        2
   quencies, high  low. A real lowpass sig-

   nal peaks at k = 0 and near k = N , and

   dips  at k  =  N  .                                                                                                    
                  2                                                                                                                  26

                                                                              k=1                    k=7 2

                                                                              positive: low  high    negative: high  low

 Interactive: the same 8 bins, centered and as computed
Zero-Padding: Same Spectrum, Finer Samples

· Zero-padding: for a length-N sequence x[n],             x[n] padded
  artificially append zeros to reach a total length        |X (ej )|
  M  N.

· Appended zeros add nothing to the DTFT sum --

the spectrum is unchanged. But the M -point                                                                                                                     n

DFT  now  samples  it  at  spacing  2  instead  of  2  :                                                                                     N               M
                                    M               N

          M -1              2
                            M
XM [k] =        x[n]   e-j     kn  = X(ej)             .

          n=0                               =   2   k
                                                M

More pixels, not more information                                                                                                                old N bins

Zero-padding interpolates the picture of the same
DTFT. It cannot resolve what the N real samples
never captured.

                                                                                                                                                                

                                                                                                                                       2        2
                                                                                                                                        M
                                                                                                                                                                   27
 Interactive: zero-pad to 2N , 4N , 8N and see the same curve sampled finer
A Complete Numeric Example (N = 4)

· Let x[n] = {1, 2, 3, 4}. With N = 4:                                            W4kn  n=0         n=1         n=2     n=3

   W4  =  e-j  2   = -j, so W4kn = (-j)kn cycles                                  k=0     1           1           1       1
                4                                                                 k=1     1          -j          -1       j
                                                                                  k=2     1          -1           1      -1
   through 1, -j, -1, j.                                                          k=3     1           j          -1      -j

· Apply X[k] =     3      x[n]W4kn :                                         |X [k]|
                   n=0

          X[0] = 1 + 2 + 3 + 4 = 10                                                     10

          X[1] = 1 - 2j - 3 + 4j = -2 + 2j                                                                           
          X[2] = 1 - 2 + 3 - 4 = -2                                                             22                   22
          X[3] = 1 + 2j - 3 - 4j = -2 - 2j                                                                   2

                                                                                                                                 k

                                                                                                1            2       3

·  Check the bins: 3 =    2·3  =  3                    -     ,  and  indeed
                            4      2                      2

                   X[3] = X[1].                                              Negative-frequency partners

 Interactive: this very x[n], with every bin to hover                        Bin 3 is bin 1's negative-frequency partner:

                                                                             for  real signals  |X [k]|  is  symmetric about  N  .
                                                                                                                              2
                                                                             (Full symmetry properties: next lecture.)

                                                                                                                                    28
Back to Physical Frequency

· The DTFT axis was normalized:  = Ts,

where  is physical frequency (rad/s) and                              |X [k]|

s    =   2      .  Undo      it  for  bin   k:
         Ts

             2               -           k  =    k   = k s .                   01         2        3  4  -3           -2     -1     ×  s
     k = N k                                     Ts        N                                                                            8

· The fold carries over in physical units: bins

0        N   span 0              s    ;  bins   N  N   span
         2                        2             2
   s      0.
-   2

· Relabeling the axis changes units, not

samples: the same N numbers, the same

fold.

 per sample = half the sampling rate                                                                                                                k
                                                                               1234567

=                         =  s   :  one 2 period of the                        positive:     =  k  s  negative:    =  (k  -  N)  s
                              2                                                                    N                             N

DTFT is one s of physical frequency, exactly                          Same stems as ever -- only the ruler above them is new (N = 8).

the  [-  s   ,     s   ]  window    from    the  DTFT  lecture.
          2         2

 Interactive: rulers under one spectrum: k    f at any sampling rate                                                                                   29
From Bins to Hertz

                                                                          |X [k]|

· The samples came from a clock: rate

fs  =    1   .      Relabel  once     more,      to  Hz:                           01         2        3   4 -3 -2 -1 kHz
        Ts

f  =      ,  so     s        fs    and the bin spacing is
       2             2       2

                f = fs =              1         1
                                            =.
                           N N Ts T0

· Bin k corresponds to:
             
             k      fs                               N
                    N                 0       k      2

    fk  =    (k -              fs     N
                               N      2
                           N)             <kN -1

· This is exactly the ordering                                                                                                                          k
                                                                                   1234567

numpy.fft.fftfreq reports, and why                                                 positive:  f  =  k  fs  negative:  f  =  (k  -  N  )  fs
                                                                                                       N                                 N
spectrum            tools  show    0  to  fs  .
                                          2

                                                                          Example: N = 8 samples at fs = 8 kHz = f = 1 kHz per bin.

 Interactive: slide a tone across the band and see which bin it lands in                                                                                   30
The Big Picture
The Square, Fully Derived

                                        continuous t                               discrete n

periodic                                CTFS             sample in t               DFS / DFT
                                                              
                           ck  =     1  T0 x(t)e-jk0tdt               X[k] =       N -1  x[n]WNkn
                                    T0                                             n=0

                           x(t) =             ck ejk0t                x[n]  =  1   N -1  X [k]WN-kn
                                        k=-                                    N   k=0

                                                                                   sample in :
                                                                                      N bins

aperiodic                               CTFT             sample in t               DTFT
                                                           spectrum
                           X(j) =          x(t)e-j t dt  2-periodic   X(ej ) =                 x[n]e-jn
                                        -                                          n=-

                           x(t)  =   1     X (j )ej t d               x[n] =    1  2 X(ej )ejnd
                                    2   -                                      2

Discrete in one domain  periodic in the other -- proven, not promised

 Sampling time made the spectrum 2-periodic. Sampling frequency (keeping N bins) made time
                                                             N -periodic.

                                                                                                         31
Summary

DFS Pair (x~[n] is N -periodic)                                         DTFT Pair

         ak    =  1        N -1  x~[n]  e-j  2  kn                            X(ej) =                 x[n]  e-jn
                  N        n=0               N                                                  n=-

         x~[n] =     N -1  ak    ej  2  kn                                        x[n] =   1    2 X(ej ) ejn d
                     k=0             N                                                    2

DFT / IDFT Pair (WN = e-j2/N )                                          The Three Bridges

         X[k] =      N -1  x[n]      WNkn                                  ·  ck  =   1  X [k]  (sampled continuous
                     n=0                                                             T0
                                                                              periodic)
         x[n]  =  1        N -1  X   [k]  WN-kn
                  N        k=0                                             · X[k] = N ak (DFT = DFS, rescaled)

                                                                           ·  X [k]  =  X(ej )  =  2  k  (DFT  samples  DTFT)
                                                                                                   N

Reading the bins -- one last time

         Bins  0     N  :  positive frequencies,    low    high.  Bins  N   N : negative frequencies, high  low.
                     2                                                  2

                                                                                                                               32
Next Class                                                  Try

             Read                                               · Compute the 4-point DFT of
                 · Oppenheim, Willsky & Nawab, §5.1 --            x[n] = {1, 0, -1, 0} by hand. Which
                    the DTFT, developed from the discrete         bins light up, and why those two?
                    Fourier series.
                 · Tan & Jiang, §4.1 -- the DFT, developed      · In numpy: compare fft(x) of a signal
                    from Fourier series coefficients of           with and without zero-padding.
                    periodic digital signals.
                                                                · Play with the interactive demos linked
                                                                  at the bottom of the slides: one lab for
                                                                  periodic signals, one for aperiodic.

Next class
Properties of the DFT -- linearity, time and frequency shifts, conjugate symmetry, Parseval's relation,
and the convolution theorem. After that: why the DFT's N 2 cost is a scandal, and the fix that was found
in 1805 -- the FFT.

                                                                                                                                                                                                        33


# Ashraf Sir/Lecture 2 - Fast Fourier Transform.pdf

The Fast Fourier Transform

Signals and Linear Systems

Ashrafur Rahman
Lecturer, CSE, BUET

ashrafur@cse.buet.ac.bd
Outline

           · Recap of Last Class
           · The Need for Speed: Naive DFT complexity
           · Fast Fourier Transform (FFT):

                     · Radix-2 Decimation-in-Time (DIT)
                     · Radix-2 Decimation-in-Frequency (DIF)
           · Conclusion: FFT Complexity Analysis

                                                                                                                                                                                                                            1
Recap of Last Class

           · In the last class we derived and looked at the DFT from 2 different perspectives.
                     · Periodic:
                             · DFT can be viewed as the evaluation of the Fourier series coefficients of a sampled periodic signal.
                             · It can also be viewed as the N unique values of the fourier series of a discrete-time periodic signal.
                     · Aperiodic:
                             · DFT can be viewed as samples of the continuous-time Fourier transform of a sampled aperiodic signal.
                             · It can also be viewed as samples of the discrete-time fourier transform of a finite-length sequence.
                     · As we will see later, if the original conginuous signal is bandlimited, we can recover the original signal from the DFT.

                                                                                                                                                                                                                            2
Naive Evaluation of the DFT

Now let's go into the computational complexity of evaluating the DFT.

· Let's examine the computational complexity of evaluating the DFT directly from its definition:

                                     N -1                                2
                                                                         N
                             X[k] =        x[n]WNkn,  where  WN  =  e-j

                                     n=0

· For each of the N values of k, we must compute:

        · N complex multiplications
        · N - 1 complex additions

· Therefore, calculating all N values of X[k] explicitly requires O(N 2) operations.
· Why is this a problem?

· Consider 1 second of audio sampled at 44.1 kHz. Here, N = 44, 100.
· The naive DFT requires roughly N 2  2 × 109 operations! This would make spectral analysis impossibly slow.

                                                                                                              3
A Brief History of the FFT                                                                             Carl Friedrich Gauss

               · 1805: Carl Friedrich Gauss                                                  James W. Cooley John W. Tukey
                          · Developed the radix-2 algorithm to interpolate asteroid orbits.                                                                 4
                          · Predates Joseph Fourier's work on harmonic analysis by over a
                             decade!
                          · Left it as a note, unpublished.

               · 1965: James Cooley & John Tukey
                          · Independently rediscovered the algorithm at IBM and Princeton.
                          · Their landmark paper launched the modern field of Digital
                             Signal Processing (DSP).

               · Many other variants of the FFT have been developed since
                  then. But we are going to study the Cooley-Tukey FFT first.
Cooley-Tukey FFT Algorithm

· The Cooley-Tukey FFT Algorithm is an elegant O(N log N ) algorithm to compute the DFT by exploiting the
  symmetry and periodicity of WN . Recall the DFT definition:

                                    N -1                                            2
                                                                                    N
                            X[k] =        x[n]WNkn  where               WN  =  e-j

                                    n=0

· We are first going to study the radix-2 FFT algorithm which­

        · Successively splits an N -point DFT into two N/2-point DFTs.
        · Assumes N is a power of 2 (if not, use zero-padding).

· There are two variants of the Cooley-Tukey FFT algorithm:

· Decimation-in-Time (DIT)
· Decimation-in-Frequency (DIF)

                                                                                                           5
Decimation-in-Time (DIT) FFT

· Decimation-in-Time splits the time-domain sequence x[n] into its even and odd indexed samples:

                                 N -1                N/2-1                   N/2-1

                    X[k] =             x[n]WNkn =              x[2r]WN2rk +         x[2r + 1]WN(2r+1)k

                                 n=0                 r=0                      r=0

·  Since  WN2rk  =  e-j  2  2rk  =  e-j   2   rk  =  WNrk/2 ,  we  get:
                         N               N/2

                                         N/2-1                           N/2-1

                                 X[k] =           x[2r]WNrk/2 +WNk              x[2r + 1]WNrk/2

                                         r=0                             r=0

                                         N/2-point DFT of evens          N/2-point DFT of odds

· So, we can compute the N -point DFT X[k] by computing two N/2-point DFTs!
· But we need some way to convert the N/2-point DFTs to N -points.

                                                                                                        6
Decimation-in-Time (DIT) FFT (cont.)

· Define new functions:

                         N/2-1

G[k] =                                x[2r]WNrk/2 = DFT{x[2r] with N/2 points}

                         r=0

                         N/2-1

H[k] =                                x[2r + 1]WNrk/2 = DFT{x[2r + 1] with N/2 points}

                         r=0

· G[k] and H[k] is clearly defined for 0  k < N/2.

· But also since N/2-point DFT is periodic with period N/2, we have:

                                      G[k + N/2] = G[k]

                                      H[k + N/2] = H[k]

· So if we copy the first half of G[k] and H[k] to the second half (periodic extension), we can write:
                                                          X[k] = G[k] + WNk H[k]

· However, we can do better.

                                                                                                        7
Decimation-in-Time (DIT) FFT (cont.)

· For the second half, N/2  k < N , we can use the property WNk+N/2 = WNk e-j = -WNk :
                                     X[k + N/2] = G[k + N/2] + WNk+N/2H[k + N/2]
                                                       = G[k] - WNk H[k] for N/2  k < N

· So, together we can write:

Radix-2 Decimation-in-Time FFT

For 0  k < N/2:

                                               X[k] = G[k] + WNk H[k]
                                      X[k + N/2] = G[k] - WNk H[k]

· This means we only need to compute the N/2-point DFTs of the even and odd parts once, and then
  combine them using simple additions/subtractions and a single complex multiplication (the "twiddle
  factor") for each output.

                                                                                                      8
DIT Butterfly Structure (N = 2)

Now let us see the computational structure of the FFT by walking through for small values of N .

· The fundamental operation is the 2-point DFT  x[0]  X [0]
  (butterfly).
                                                x[1]  -1 X[1]
· Note that W20 = 1.

    X[0] = x[0] + x[1]W20 = x[0] + x[1]
    X[1] = x[0] - x[1]W20 = x[0] - x[1]

                                                                                                  9
DIT Butterfly Structure (N = 4)                                                    G[0]      X [0]
                                                            x[0]
           · A 4-point DFT is built from two 2-point DFTs.
           · G[k] and H[k] (outputs of Stage 1) are         x[2] W20 -1 G[1]                 X [1]

              combined using twiddle factors W4k.           x[1]  H[0] W40               -1  X [2]
      Explicit Formula:
                                                            x[3] W20 -1 H[1] W41         -1  X [3]
                       X[0] = G[0] + W40H[0]
                       X[1] = G[1] + W41H[1]
                       X[2] = G[0] - W40H[0]
                       X[3] = G[1] - W41H[1]

                                                                                                    10
DIT 8-Point FFT: First Iteration
           · For N = 8, the sequence is split into N/2 = 4-point DFTs of even and odd indices.
           · The outputs G(k) (evens) and H(k) (odds) are combined using the relation:
           · X[k] = G(k) + W8kH(k) and X(k + 4) = G(k) - W8kH(k) for k = 0, . . . , 3.

                                                                                                                                                                                                                           11
DIT 8-Point FFT: Full Algorithm
           · Expanding all 4-point and 2-point DFTs yields the complete 8-point DIT structure.
           · Notice the inputs are in bit-reversed order, while outputs are in natural order.

                                                                                                                                                                                                                          12
Understanding Bit-Reversed Order

· In Radix-2 DIT FFT, the inputs appear in bit-reversed order.

· Why? The sequence is successively divided into even and odd indexed halves.
· For N = 8, the physical movements happen in three stages:

       1. Stage 1: Even (0,2,4,6), Odd (1,3,5,7)
      2. Stage 2: Even-Even (0,4), Odd-Even (2,6), Even-Odd (1,5), Odd-Odd (3,7)
      3. Stage 3: Single elements: x[0], x[4], x[2], x[6], x[1], x[5], x[3], x[7]

Original Index                    Binary  Bit-Reversed Binary  New Position

        0                          000              000               0
        1                          001              100               4
        2                          010              010               2
        3                          011              110               6
        4                          100              001               1
        5                          101              101               5
        6                          110              011               3
        7                          111              111               7

· Putting even before odd corresponds to sorting by the rightmost bit.
· Putting even-even before odd-even corresponds to sorting by the second rightmost bit, and so on.
· This is equivalent to sorting the input sequence by the bit-reversed order of their indices.

                                                                                                                                                                                                           13
Radix-2 DIT FFT: Pseudocode & Complexity

             Iterative Radix-2 DIT FFT

                 Bit-reverse array x of length N (N = 2v )
                 for s = 1 to log2 N : // For each stage

                      M = 2s // 2, 4, 8, ..., N
                      WM = e-j2/M
                      for l = 0 to N - M step M : // M -point DFT blocks in same stage

                         W = 1 // Twiddle factors
                         for k = 0 to M/2 - 1: // Butterfly operation

                            g = x[l + k] // G[k]
                            h = W · x[l + k + m/2] // WM k H[k]
                            x[l + k] = g + h // X[k]
                            x[l + k + m/2] = g - h // X[k + m/2]
                            W = W · Wm

      Complexity Analysis:

           · Bit-Reversal: Takes O(N ) operations.
                     · Swap x[k] with x[k] where k is the bit-reversal of k.

           · Outer Loop: Runs log2 N times (stages).
           · Inner Loops: Combined, they iterate over all N elements, performing N/2 butterflies per stage.
           · Total Complexity: O(N log2 N) complex multiplications and additions.

                                                                                                                                                                                                                          14
Decimation-in-Frequency (DIF) FFT: Derivation

We now study the second variant.

· Instead of separating even/odd time indices, Decimation-in-Frequency splits the summation
  n = 0 . . . N - 1 into the first half and second half of time indices:

                                        N/2-1              N -1

                                X[k] =         x[n]WNkn +         x[n]WNkn

                                        n=0                n=N/2

                                        N/2-1              N/2-1

                                   =           x[n]WNkn +         x[n + N/2]WNk(n+N/2)

                                        n=0                n=0

·  Since  WNkN/2  =  e-j  2  k  N  = e-jk = (-1)k, we have:
                          N     2

                                           N/2-1

                                   X[k] =         x[n] + (-1)kx[n + N/2] WNkn

                                             n=0

· Now, we decimate in the frequency domain by evaluating even and odd k.

· Even k = 2m: (-1)2m = 1, and WN2mn = WNm/n2

                                        N/2-1

                          X[2m] =              (x[n] + x[n + N/2]) WNm/n2 = DFTN/2{a(n)}

                                        n=0
                                                                a(n)

                                                                                                                                                                                  15
DIF FFT Derivation (Cont.)

· Odd k = 2m + 1: (-1)2m+1 = -1, and WN(2m+1)n = WNn WN2mn = WNn WNm/n2

                                         N/2-1

                            X[2m + 1] =         (x[n] - x[n + N/2]) WNn WNm/n2 = DFTN/2{b(n)}

                                         n=0

                                                b(n)

· The fundamental butterfly sequence performs additions before the multiplication by the twiddle factor
  WNn :

                                                                                                         16
DIF 8-Point FFT: Full Algorithm
           · Expanding the layers gives the full 8-point DIF structure.
           · Here inputs are in natural order, while outputs emerge in bit-reversed order.

                                                                                                                                                                                                                          17
Why Zero-Pad? The Practical Necessity

             The Radix-2 Requirement
             Radix-2 FFT algorithms require the sequence length N to be exactly a power of 2 (N = 2m).

      The Problem:
           · Real-world data often consists of M samples, where M is not a power of 2.
           · If we restrict ourselves to M samples, we are stuck with the slow O(M 2) naive DFT!

      The Solution: Zero-Padding
           · We simply append zeros until we reach the next power of 2: N = 2log2 M.
           · Bonus: Zero-padding interpolates the spectrum, giving a smoother visualization without altering the true
              frequency content X(ej).
           · However, if used for periodic x[n], zero-padding changes the period and shape of the periodic signal.
           · Can we do FFT without zero-padding?

                                                                                                                                                                                                                          18


# Ashraf Sir/Lecture 3 - DFT Properties and Applications.pdf

DFT Properties and Applications

Signals and Linear Systems

Ashrafur Rahman
Lecturer, CSE, BUET

ashrafur@cse.buet.ac.bd
Recap of Last Class

                                                             |X [k]|

                                                                      positive, low  high     negative, high  low

   DFT / IDFT Pair (WN = e-j2/N )

        X[k] =          N -1  x[n]   WNkn
                        n=0

        x[n]   =     1     N -1      X [k]  WN-kn                                                                       k
                     N     k=0
                                                                                           N             N -1

                                                                                           2

·  Three bridges: ck       =   1     X  [k],  X[k] = N ak,   How to read N bins
                              T0
   and               X (ej )            k.
        X [k]  =              =      2
                                     N
                                                             Bins 0   N  :  positive frequencies.  Bins  N          N:
·  Bin k lives at f     =  k  fs  ;  spacing  f    =  fs  .           2                                  2
                              N                       N      folded negative frequencies. A real lowpass signal

                                                             peaks at k = 0 and near k = N .

                                                                                                                           1
Outline

           · Part I -- The rules of the game: how the DFT behaves when a signal is shifted, flipped, modulated, or real
              -- on N points everything wraps.
                     Linearity, circular shifts, modulation, conjugate symmetry, Parseval.

           · Part II -- The payoff: multiplying DFTs convolves signals -- circularly, around the same clock. We will see
              the wrap, picture it, and then defeat it: zero-padding turns circular convolution into the linear
              convolution every filter needs.

             One lecture, one theme
             Last class we built the DFT. Today we learn its grammar -- and cash it in: filtering signals by multiplying
             spectra.

                                                                                                                                                                                                                           2
The Rules of the Game
Everything Lives on a Clock

· The DFT only ever sees N numbers. Synthesis rebuilds                              n=0
  them N -periodically: evaluating the IDFT at n + N
  gives back x[n]. (Recall why: sampling in frequency, N                         7  n increases  1
  bins, forced periodicity in time.)                              n=8 lands
                                                                                    N =8            2
· So indices live on a clock: define ((n))N  n mod N --            on n=0
  e.g. ((9))8 = 1 and ((-1))8 = 7.
                                                                         6
· Tiling the N samples forever -- one clock lap per copy
  -- gives the periodic extension:                                5                              3

             x~[n]  x[((n))N ], x~[n + N ] = x~[n].                                 4

  It matches x[n] on 0, . . . , N - 1 -- the copy of x the DFT    Same clock for the bins k -- we proved X[k + N ] = X[k]
  really works with.                                                                                last time.

 The theme of Part I

  Nothing falls off the end of N points -- it wraps: every shift
  becomes a rotation of the clock.

                                                                                                                           3
Warming Up: Two Properties for Free

· Every property today comes straight from the analysis sum -- nothing else is needed:

                                             N -1

                                     X[k] =        x[n] WNkn.

                                             n=0

· Linearity. The sum is linear in the samples, so a x[n] + b y[n]  a X[k] + b Y [k].1

· Periodicity. WN(k+N)n = WNkn, so X[k + N ] = X[k] -- proved last lecture. The bins live on the same
  clock as the samples.

· Everything else in Part I -- shifts, reversal, symmetry, energy -- falls to a single move:

The one proof move of the day

Substitute into the DFT sum, re-index, and let the clock absorb whatever spills past the edge: both x~[n]
and WNkn are N -periodic, so any window of N consecutive terms gives the same sum.

1Both sequences must have the same length N -- pad the shorter one with zeros first. Remember this; it returns in Part II.
                                                                                                                                                                                                                4
Circular Time Shift

· Shift the periodic extension by m, take the DFT, substitute        x7  x0
  r = n - m:                                                   x6                      x1

N -1                   N -1-m                                            rotate m
                                                                                              x2
      x~[n - m] WNkn = WNkm         x~[r] WNkr = WNkm X[k].

n=0                          r=-m

· The window slid to r = -m, . . . , N - 1 - m -- but          x5        x3
  x~[r] WNkr is N -periodic, so any N consecutive terms give
  the same total: it is still X[k]. The wrap is invisible.                           x4
                                                               a shift is a rotation: every sample survives

Circular time shift                                            Phase only

x[((n - m))N ]         WNkm  X [k]  =  e-j  2  km  X [k]       |WNkm| = 1: shifting changes no
                                            N                  magnitude, only phase. Where a sig-
                                                               nal sits in time lives entirely in X[k].

                                                                                                             5
Frequency Shift (Modulation)

· The mirror-image property -- multiply by a complex tone in time, and the spectrum rotates:

                                 WN-k0 n  x[n]  =  e  j  2  k0 n  x[n]    X[((k - k0))N ].
                                                         N

· Same one-line proof, run on the other side: absorb WN-k0n into WNkn, and k - k0 appears.

·  Concrete special case, k0     =  N  :  e jn = (-1)n, so flipping every other sign slides the spectrum by half
                                    2
   the clock -- low and high frequencies trade places:

   |X[k]|: lowpass                                                        after ×(-1)n : highpass

                                                         ×(-1)n

                                                   k                                                     k

                              N           N -1                            N                        N -1

                              2                                           2

                                                                                                                  6
Time Reversal and Conjugation

· Reversal -- playing the clock backwards (0 stays, 1  N -1, 2  N -2, ...) hands the minus sign to k.
  Substitute r = -n, then slide the window (the one move):

N -1                           0

      x~[-n] WNkn =                 x~[r] WN(-k)r = X[((-k))N ]        x[((-n))N ]  X[N - k].

n=0   r=-(N -1)

· Conjugation -- conjugating the sum flips the kernel to the -k one, WNkn  = WN(-k)n:

N -1                           N -1                 = X[((-k))N ]      x[n]  X[N - k].

      x[n] WNkn =                    x[n] WN(-k)n

n=0                            n=0

· Now let x[n] be real: x[n] = x[n], so its DFT must equal the conjugation result:

Real signal  conjugate-symmetric spectrum

      X[k] = X[((-k))N ]  X[N - k] = X[k].

· Half the bins are forced by the other half. Next slide: what this does to |X[k]| and X[k] -- last lecture's
  bin-reading mantra, proved.

                                                                                                                                                                                                            7
Conjugate Symmetry: Why Real Signals Fold

· We just proved X[N - k] = X[k]. In polar form,

   that  is  two  symmetries  about  k  =                  N  :
                                                           2

   |X[N - k]| = |X[k]|               magnitude even,                         |X [k]|

                                                                                         even about  N
                                                                                                     2
   X[N - k] = -X[k] phase odd.

· Check on last lecture's x = {1, 2, 3, 4},                                  X [k]    N              N -1
  X = {10, -2+2j, -2, -2-2j}: indeed
  X[3] = -2 - 2j = X[1].                                                              2

·  Only bins k =     0(,C.o.r.o,llN2arya:rerefarel ean--d  the upper  half            N  odd about   NN -1
   is their mirror.                                        even x~    X [k]           2              2

   real.)                                                                    the 8-point DFT of the real sequence {3, 5, 2, 0, 1, 2, 4, 1}

· This is why the fold picture works: bin N - k is
  bin k's negative-frequency partner.

 Interactive: any real signal you draw comes out symmetric about  =                                                                         8
Parseval's Relation: Energy Is Re-Bookkept

   Parseval's relation

                                         N -1  |x[n]|2  =  1  N -1  |X [k]|2
                                         n=0               N  k=0

· Proof in one substitution (sums run 0 to N -1): swap x[n] for the conjugated IDFT, exchange the sums:

          x[n] x[n] =         x[n] ·  1        X[k] WNkn   =  1     X  [k]       x[n] WNkn  =  1      |X [k]|2 .
                                                              N                                N
       n                  n           N  k                       k            n                    k

                                                                                 = X[k]

· Check on x = {1, 2, 3, 4}:  time side 1 + 4 + 9 + 16 = 30;     bin side     100+8+4+8  =  30.  
                                                                                      4

·  So  |X [k]|2  is the energy sitting in bin k -- the power spectrum.
           N

   Why it had to be true

   The N tones WN-kn are orthogonal: the DFT is a change of basis in CN , and orthogonal moves re-
   bookkeep energy -- they never create or destroy it.

                                                                                                                  9
The Property Table

                    Property              Time domain                       DFT domain

                    linearity             a x[n] + b y[n]                   a X[k] + b Y [k]
                    circular time shift                                     WNkm X[k]
                    modulation            x[((n - m))N ]                    X[((k - k0))N ]
                    time reversal         WN-k0n x[n]
                    conjugation                                             X[((-k))N ]
                    real signal           x[((-n))N ]                       X[((-k))N ]
                    duality               x [n]                             X[N - k] = X[k]
                    circular convolution
                    multiplication        x[n]  R                           N x[((-k))N ]
                    Parseval              X[n] (bins replayed as a signal)

                                          xh                                X[k] H[k]  Part II

                                          x[n] h[n]                          1  X  H
                                                                            N
                                                 |x[n]|2                        1         |X [k]|2
                                              n                             =   N      k

One table to keep

Every row follows from the DFT sum by the same move: re-index, and the clock absorbs the wrap. The two convolution
rows are the rest of today.

                                                                                                                    10
Filtering with the DFT
Why Convolution Matters

           · From the first half of the course: an LTI system is completely described by its impulse response h[n], and
              its output is the linear convolution

                                                            y[n] = (x  h)[n] = x[m] h[n - m].

                                                                                                                     m

           · Every filter you will ever run -- smoothing, echo, equalizer -- is this sum.
           · Lengths add: x of length L, h of length M  y of length L + M - 1. Direct cost: about L · M

              multiplications.

x[n]  LTI system: h[n] y[n] = x  h

The dream
In every Fourier world so far, convolution in time became multiplication of spectra. If that holds for
the DFT, filtering becomes: transform, multiply N numbers, transform back. Does it hold? Almost.

                                                                                                                                                                                                         11
What Multiplying DFTs Actually Does

· Take two length-N sequences, multiply their DFTs bin by bin, and invert. What signal is that?

         1  N -1                                1  N -1    N -1
         N                                      N
y[n]  =           X[k] H[k] WN-kn            =                   x[m] WNkm H[k] WN-kn

            k=0                                    k=0 m=0

          N -1              1        N -1                  -- the IDFT of H, evaluated at n - m.
                            N
      = x[m]                               H[k] WN-k(n-m)

          m=0                        k=0

· But n - m can be negative -- and the IDFT evaluated off the grid returns the periodic extension:
  WN-k(n-m+N) = WN-k(n-m), so the inner sum is h~[n - m] = h[((n - m))N ].

                                             N -1

                                     y[n] =        x[m] h[((n - m))N ].

                                             m=0

The wrap arrives uninvited

This is almost convolution -- but the index into h wraps around the clock. Multiplying DFTs convolves
circularly.

                                                                                                       12
Circular Convolution: Two Wheels

Circular convolution theorem (both sequences length N )

                                     N -1

(x  h)[n]                                                 x[m] h[((n - m))N ]          X[k] H[k]

                                     m=0

· Flip, slide, multiply, add -- but on the clock: x rides the outer wheel, h sits backwards on the inner. One
  output = rotate one tick, multiply across the spokes, add.

             n=0                                                               n = 1: rotate one tick
               2                                                                           2

   1                                                      4                    1       4
                                                               5
                                  21                                              121

2                                 1                               2                                    5

   3                                                      6                    3       6

                                             5                                             5
                                  y[0] = 1·2 + 2·1 + 1·2 = 6      y[1] = 1·4 + 2·2 + 1·1 = 9

x = {2, 4, 5, 6, 5, 3, 2, 1}, h = {1, 2, 1} -- slate = taps that wrapped

 Interactive: spin the wheels yourself, output by output                                                       13
Step 1 -- Linear: the Off-Edge Taps Find Nothing

           · Linear convolution at n = 0: y[0] = m x[m] h[0 - m]. Flipping h = {1, 2, 1} puts taps at m = 0, -1, -2:

                                                                                     x[m] -- it only exists for m = 0, . . . , 7
                                                nothing lives

                                                    up here

        -2 -1 0  3                                                                   m
                                                      7

h[n-m]           flipped h: three real taps

                                                                                                                     m
        -2 -1 0

        y[0] = 1 · x[0] + 2 · x[-1] + 1 · x[-2] = 2

                 nothing                     nothing

How linear convolution treats the edge
Taps hanging past the edge multiply nothing -- their terms are silently dropped. (Hence the L + M - 1-long output.)

                                                                                                                                  14
Step 2 -- Circular: the Taps Wrap to the Right
           · The circular sum, y[0] = m x[m] h[((0 - m))N ], reads indices on the clock: ((-1))8 = 7 and ((-2))8 = 6.
              The off-edge taps are not dropped -- they are moved:

                                                                                            same x[m]

                                the wrapped taps land on x's tail

                                                                       m

                -2 -1 0  3  67

                                wrap right:

h[((n - m))N ]                  ((-1))8 = 7
                                ((-2))8 = 6 m

                -2 -1 0     67

                y[0] = 1 · x[0] + 2 · x[7] + 1 · x[6] = 2 + 2 + 2 = 6

How the mod treats the edge

Nothing is dropped: every off-edge tap is folded back into 0, . . . , N - 1 and multiplies the other end of x. That fold
is the entire difference between circular and linear.

                                                                                                                          15
Step 3 -- Equivalently: Extend x to the Left

· Same products, read the other way: leave the taps where they fell. The wrapped values x[7], x[6] are
  exactly what the periodic extension x~ puts at m = -1, -2:

                        the previous lap of x~ -- the tail, waiting       the N kept samples

                        -8                            -2 -1 0                                                                  m
                                                                                                       7

                                                                          the taps, untouched -- as in Step 1

                                                                                                                                                      m
                                                                -2 -1 0

                     y[0] = 1 · x~[0] + 2 · x~[-1] + 1 · x~[-2] = 2 + 2 + 2 = 6 -- identical

Two readings of one sum

        x[m]  h[((n  -  m))N ]  =          h[j] x~[n  -  j]:  wrap   the  taps  right,  or  extend  x  left.  And  periodically                          extending  x  is

     m                                  j
just... (next slide).

                                                                                                                                                                           16
Unwinding the Clock

          cut                                               the lap before     one lap                  the lap after
         here
                                    unroll                                  0           78                                         m
                      0                                 -8                                                             15
               7
                                                                            one full turn of the wheel
                             3

      x, wrapped around the clock:
walking past m = 7 lands on m = 0

Same trip, two pictures

Going round and round the wheel is walking along the periodic extension x~. So circular convolution has two equal
readings: rotate the flipped h on the clock, or slide the flipped h along the unrolled x~. Next, both compute our
example.

                                                                                                                                      17
Worked Example: Circular = Linear

· Our running pair: x = {2, 4, 5, 6, 5, 3, 2, 1},                    the lap before -- the tail, waiting  the N kept samples
  h = {1, 2, 1}; L = 8, M = 3.
                                                                     -8  -2-1 0                                                                      m
· Linear (length 8 + 3 - 1 = 10):                                                                                             7

            {2, 8, 15, 20, 22, 19, 13, 8, 4, 1}                                                           flipped h at n=0    slides right

· Circular (length 8):                                                                                                                              m
                                                                         -2-1 0
         x  h = {6, 9, 15, 20, 22, 19, 13, 8}
                                                                         y[0] = 1 · 2 + 2 · 1 + 1 · 2 = 6 (should have been 2)
· Six values agree; the first two are corrupted
  -- one per off-edge tap: on the unrolled                               the window caught the previous lap's tail -- that is the wrap
  clock, the sliding h grabs the previous lap's
  tail samples 1 and 2.

 Interactive: slide the flipped h along the unrolled clock yourself                                                                                     18
Zero-Padding Makes It Linear

· Circular convolution is the linear result    padded to N = 10: the previous lap now ends in zeros
  folded mod N -- time aliasing. If the
  linear result fits, nothing folds:             00                                                             m
                                               -2 -1 0
 The zero-padding rule                                                                                 7     9

       Pad both sequences to length                                                  flipped h at n=0: y[0] = 1 · 2 + 2 · 0 + 1 · 0 = 2 
      N  L + M - 1 and circular                                                                                                                        m

          convolution equals linear            -2 -1 0
                   convolution.
                                                                                                 2  4
· Padded to N = 10, the circular result is                                              0                 5
  the linear list: {2, 8, 15, . . . , 4, 1}.                                                              6
                                                                                     0        21                   the wheel agrees:
· The zeros aren't data -- they are room for                                                                       the wrapped taps
  the tail. (Last lecture padding bought                                                   1                    point at padded zeros
  finer DTFT samples; today it buys
  correctness.)                                                                      1

                                                                                        2           5

                                                                                              3

 Interactive: turn on padding in any of the three views and watch the wrap go quiet                                                                       19
The Filtering Recipe

 Fast filtering with the DFT (input length L, filter length M )

    1. Choose N  L + M - 1; zero-pad both x and h to length N .
    2. Compute X[k] and H[k] (N -point DFTs).
    3. Multiply bin by bin: Y [k] = X[k] H[k].
    4. Invert: y[n] = IDFT{Y }; the first L + M - 1 samples are the linear convolution.

· Honest accounting, today: each DFT costs  N 2 multiplications, so this loses to the direct L · M sum.
  The transform is the bottleneck.

· In scipy, signal.fftconvolve is this recipe. (For streaming audio, block variants like overlap-add run
  it chunk by chunk -- advanced FFT lecture.)

 Why this row of the table changed engineering

 Next class the FFT drops each transform to  N log2 N -- and this recipe becomes the fastest known
 way to convolve.

 Interactive: step through convolution, sample by sample                                                  20
The Big Picture
Summary

Properties: everything wraps                         The pictures to remember

         · x[((n - m))N ]  WNkmX[k] (phase only)         · the clock: indices mod N ; shifts are
                                                           rotations
         · WN-k0nx[n]  X[((k - k0))N ]
         · real x[n]: X[N - k] = X[k] (the fold)         · two wheels: rotate, multiply, add =
                                                           xh
         ·  n |x[n]|2    =  1  k |X[k]|2
                            N                            · sliding on x~: the neighbouring copy
                                                           leaking into the window is the wrap;
The two theorems that matter                               padding replaces it with zeros

         ·  x  h  X[k]H[k],    x[n]h[n]     1  X  H  Today in one sentence
                                            N
                                                     On N points everything wraps -- pad for the
         · circular = linear iff N  L + M - 1        wrap, and the DFT turns filtering into multiplica-
                                                     tion.
            (zero-pad!)
                                                                                                                                                 21
Next Class                                                  Try

             Read                                               · Compare np.convolve(x, h) with
                                                                  ifft(fft(x) * fft(h)) --
                 · Oppenheim, Willsky & Nawab, Problem            unpadded, then padded to L + M - 1.
                    5.53 -- the DFT, built as a worked
                    exercise. (§5.3­5.5 state today's           · Verify Parseval and conjugate
                    properties in DTFT notation, if you           symmetry on any real signal you like.
                    want a second telling.)

                 · Tan & Jiang, §4.1 -- another telling of
                    the DFT and its bins, with worked
                    numbers.

Next class

The DFT costs N 2 multiplications -- for a one-second audio clip, that is already billions. Next class: the
divide-and-conquer trick Gauss scribbled in 1805 and the world rediscovered in 1965 -- the Fast Fourier
Transform.

                                                                                                             22


# Ashraf Sir/Lecture 4 - Advanced FFT.pdf

Advanced FFT Algorithms and Applications

Signals and Linear Systems

Ashrafur Rahman
Lecturer, CSE, BUET

ashrafur@cse.buet.ac.bd
Recap of the Last Two Classes                                Lecture 2 -- filtering with the DFT

             Lecture 3 -- the FFT                                · x  h  X[k]H[k]; pad to
                                                                   N  L + M - 1 and circular = linear.
                 · Radix-2 DIT: split x[n] into evens and
                    odds, combine with the butterfly             · The recipe: pad, transform, multiply,
                                     X[k] = G[k] + WNk H[k]        invert.
                           X[k + N/2] = G[k] - WNk H[k]
                                                                 · Honest accounting then: each DFT
                 · Cost drops from N 2 to N log2 N .               cost N 2, so the recipe lost to the
                 · But it needs N = 2m. Otherwise we               direct L · M sum.

                    zero-pad -- which changes a periodic
                    signal.

Today's two questions
   1. Can we have an FFT for any N -- powers of 3, mixed factors, even primes -- without padding?
  2. With the FFT in hand, how fast does the filtering recipe become?

                                                                                                                                                                                                          1
Outline

           · Advanced FFT Algorithms
                     · Radix-2 and Radix-3 DIT: the tabular (matrix) interpretation
                     · General Cooley­Tukey factorization N = N1N2 and Bailey's four-step FFT

           · Application: Fast Convolution
                     · The Lecture-2 filtering recipe, now with the FFT
                     · Complexity: O(N log N ) versus O(LM )

           · FFT for Prime N : Bluestein's Algorithm
                     · The chirp-z identity: a DFT is a linear convolution
                     · Padding the chirp without breaking the wrap

                                                                                                                                                                                                                           2
Advanced Matrix Interpretations of the
FFT
Revisiting Radix-2: A Tabular View

           · Previously, we derived Radix-2 DIT purely algebraically.
           · We divided the input into even and odd indices and calculated their DFTs G[k] and H[k].
           · Then we combined them using the butterfly operation:

                                                                          X[k] = G[k] + WNk H[k]
                                                                 X[k + N/2] = G[k] - WNk H[k]
           · We can think about this in a different, more visual way--one that leads to an elegant generalization.
           · Key Idea: Reshape the 1D input x[n] into a 2D matrix, perform DFTs along rows and columns.

                                                                                                                                                                                                                            3
Radix-2 DIT: Column-Major Input & Row DFTs

· Let us arrange x[n] into a 2 × N/2                            Column-Major Input x[n]
  matrix in column-major order:
                                                        n2 = 0  n2 = 1  n2 = 2           ···
                    n = 2n2 + n1
   Where,                                      n1 = 0   x[0]    x[2]    x[4]             ···           DFT
   n1 = row index  {0, 1}                       (Even)                                                 DFT
   n2 = column index  {0, 1, . . . , N/2 - 1}
                                               n1 = 1   x[1]    x[3]    x[5]             ···   1st DFTs
· Row 0 (n1 = 0): Even indices                   (Odd)                                         N/2-pt
· Row 1 (n1 = 1): Odd indices                                                                 (row-wise)
· 1st DFT: Then perform N2-point DFTs                           After Row-wise DFT

  along each row ().                                    n2 = 0  n2 = 1  n2 = 2           ···
       · Row 0  G[k]
       · Row 1  H[k]                           n1 = 0   G[0]    G[1]    G[2]             ···
                                                (Even)

                                               n1 = 1   H [0]   H [1]   H [2]            ···
                                                 (Odd)

                                                                                                            4
Radix-2 DIT: Twiddle Factors & Column DFTs

                                                                         After Twiddle Factors

                                                               n2 = 0    n2 = 1    n2 = 2       ···

· After row DFTs, multiply row n1 by twiddle factors  n1 = 0   G[0]      G[1]      G[2]         ···
  WNn1 k .                                             (Even)
       · Row 0: ×WN0 = 1
       · Row 1: ×WNk                                  n1 = 1   H [0]WN0  H [1]WN1  H [2]WN2     ···
                                                        (Odd)
· 2nd DFT: Perform 2-point DFT down each column ().

· This is exactly the butterfly!

   X[k] = G[k] + WNk H[k]                                      DFT       DFT       DFT          DFT

X  [k +  N  ]  =  G[k]            -  WNk  H [k]
         2
                                                                         After Column-wise DFT
· We obtain the DFT of the original sequence x[n]!
                                                               n2 = 0    n2 = 1    n2 = 2       ···

· Row 0 gives X[0 . . . N/2-1],                       n1 = 0   X [0]     X [1]     X [2]        ···
  row 1 gives X[N/2 . . . N -1].                       (Even)

· But the output occurs in row-major order.

                                                      n1 = 1   X[N/2] X[1 + N/2] X[2 + N/2]     ···
                                                        (Odd)

                                                                                                     5
Radix-2 DIT: Reading the Output Row-Major                                      After Output Indexing

       · We want X[k] in the correct order. We want the                k2 = 0  k2 = 1  k2 = 2           ···
          transpose matrix.
                                                               k1 = 0  X [0]   X [1]   X [2]            ···
       · Mathematically, for
                  k1 = row index  {0, 1}                       k1 = 1 X[0 + N/2] X[1 + N/2] X[2 + N/2]  ···
                  k2 = column index  {0, . . . , N/2 - 1}

       · We want the row-major indexing:

                                    k = (N/2)k1 + k2

       · Using this index, we can write:
                X[(N/2)k1 + k2] = G[k2] + W2k1 WNk2 H[k2]

       · Not the final form yet!
       · But key take away: We can visualize the Cooley­Tukey

          algorithm as arranging numbers on a matrix,
          performing DFTs on rows and columns!

                                                                                                             6
Radix-3 DIT DFT: Derivation

· The same idea extends naturally. For N = 3N2, split x[n] into three subsequences by index modulo 3:

        N/3-1                                    N/3-1                           N/3-1

X[k] =                       x[3r] WNrk/3 + WNk         x[3r + 1] WNrk/3 + WN2k         x[3r + 2] WNrk/3

        r=0                                      r=0                             r=0

· Define three N/3-point DFTs:

                                      N/3-1

                             Gm[k] =             x[3r + m] WNrk/3  m  {0, 1, 2}

                                      r=0

Radix-3 DIT Combination

                                                    X[k] = G0[k] + (WNk G1[k]) + (WN2k G2[k])
                                X[k + N/3] = G0[k] + W31(WNk G1[k]) + W32(WN2k G2[k])
                              X[k + 2N/3] = G0[k] + W32(WNk G1[k]) + W34(WN2k G2[k])

· The above 3 equations are also a 3-point DFT!

                                                                                                                                                                                                            7
Radix-3 DIT: Tabular Interpretation (N1 = 3, N2 = N/3)

 · Load x[n] into a 3 × N/3 matrix,                             Column-Major Input
   column-major: n = 3n2 + n1.
                                                        n2 = 0  n2 = 1  n2 = 2               ···
 · Row 0: n  0 (mod 3)
 · Row 1: n  1 (mod 3)                 n1 = 0 x[0]              x[3]    x[6]                 ···  G0
 · Row 2: n  2 (mod 3)
                                                                                                      1st DFTs
1. 1st DFTs: N/3-point DFT along each
   row ().                             n1 = 1 x[1]              x[4]    x[7]                 ···  G1  N/3-pt

2. Multiply by twiddle WNn1k2 .                                                                       ()
3. 2nd DFTs: 3-point DFT down each
                                       n1 = 2 x[2]              x[5]    x[8]                 ···  G2
   column ().
                                                                2nd DFTs: 3-pt () + twiddle
 · Take output row-major:
   k = (N/3) k1 + k2.

                                                                                                                8
General Cooley­Tukey Factorization (N = N1N2)

· Having seen the tabular view for Radix-2 and Radix-3, let's formalize the general N1 × N2 factorization.
· Re-index the input n as an N1 × N2 matrix in column-major order:

n = N1n2 + n1                                  n1  {0, 1, . . . , N1 - 1}
                                               n2  {0, 1, . . . , N2 - 1}

Substituting this into the DFT definition yields a 2D sum:

        N1-1 N2-1                              x[N1n2 + n1] WN(N1n2+n1)k

X[k] =

        n1=0 n2=0

· Re-index the output k as an N1 × N2 matrix in row-major order:

k = N2k1 + k2                                  k1  {0, 1, . . . , N1 - 1}
                                               k2  {0, 1, . . . , N2 - 1}

                                                                                                            9
General Cooley­Tukey Factorization (N = N1N2)

· Substitute k = N2k1 + k2 into the exponent (N1n2 + n1)k:

                  (N1n2 + n1)(N2k1 + k2) = N1N2n2k1 + N1n2k2 + N2n1k1 + n1k2
                                                     = N n2k1 + N1n2k2 + N2n1k1 + n1k2

· The first term is a full turn: WNNn2k1 = e-j2n2k1 = 1, so this cross term vanishes.
· The remaining three factors are each a root of unity of a different order:

                  WNN1n2k2 = WNn22k2 ,          WNN2n1k1 = WNn11k1 ,  WNn1k2 (stays as it is)

since  WNN1 m  =  e-j     2   N1 m  =  e-j  2   m  =  WNm2 .
                       N1 N2                N2

· Hence                       WN(N1n2+n1)(N2k1+k2) = WNn22k2 · WNn1k2 · WNn11k1

· Substituting this back into the double sum and rearranging:

                                                                                               10
General Cooley­Tukey Factorization (N = N1N2)

Cooley­Tukey 2D Matrix Formulation

                N1 -1                            N2 -1                   

X[N2k1 + k2] =                      WNn1k2              x[N1n2 + n1] WNn22k2  WNn11k1

                n1=0 twiddle                     n2 =0

                                                 N2-point DFT of row n1

· Inner sum: an N2-point DFT along each row of the N1 × N2 input matrix (over n2, indexed by k2).
· Twiddle factors: the entry at (n1, k2) is scaled by WNn1k2 .
· Outer sum: an N1-point DFT down each column of the intermediate matrix (over n1, indexed by k1).
· Read the result row-major: k = N2k1 + k2.

                                                                                                    11
Bailey's FFT Algorithm

           · The Cooley­Tukey matrix formulation directly yields Bailey's FFT (a.k.a. the Four-Step FFT):

             Bailey's FFT

                1. Arrange input x[n] in an N1 × N2 matrix (column-major).
                2. Compute N2-point DFT of each row ().
                3. Multiply entry (n1, k2) by twiddle factor WNn1k2 .
                4. Compute N1-point DFT of each column ().

           · How to compute the N1- and N2-point DFTs? Apply the same algorithm recursively!
           · If N = p1a1 pa22 · · · , we recursively factor until only small primes remain  O(N log N ) for any composite

              N.
           · This handles powers of 2, powers of 3, mixed radices--any N with small prime factors.
           · But what if N itself is a large prime? Hold that question: the answer needs a tool we can now build -- fast

              convolution.

                                                                                                                                                                                                                          12
Application: Fast Convolution
The Filtering Recipe, Now With the FFT

           · Lecture 2: LTI filtering is the linear convolution y = x  h (L input samples, M taps), costing L · M
              multiplications directly.

           · Multiplying DFTs gives circular convolution; zero-padding to N  L + M - 1 parks the wrapped taps on
              zeros, so circular = linear.

           · The transform was the bottleneck: N 2 per DFT. Replace every DFT by an FFT.

             Fast Convolution (input length L, filter length M )

                1. Choose N  L + M - 1 -- the next power of 2, so Radix-2 applies.
                2. Zero-pad x and h to length N .
                3. X[k] = FFT{x} and H[k] = FFT{h}.
                4. Multiply bin by bin: Y [k] = X[k] H[k].
                5. y[n] = IFFT{Y }; keep the first L + M - 1 samples.

           · Padding beyond L + M - 1 is harmless: the extra room only appends trailing zeros to y. (Contrast Lecture
              3, where padding a periodic signal changed its period -- here nothing is periodic, so nothing breaks.)

                                                                                                                                                                                                                          13
Fast Convolution: Complexity Analysis

           · How much faster is this really?
           · Direct Linear Convolution: takes O(L · M ) operations. If L  M  N/2, naive convolution takes roughly

              O(N2) steps.
           · Fast Convolution (using Radix-2 FFT):

                     · 2 forward FFTs: 2 × O(N log N )
                     · 1 element-wise multiplication: O(N )
                     · 1 inverse FFT: O(N log N )
              Total time: O(N log N) complex multiplications.

             Real-world magnitude

             Applying a 1-second reverb filter (L = 44,100) to 1 second of audio (M = 44,100):
                 · Naive: L × M  1.94 × 109 operations.
                 · Fast Convolution: padding to N = 131,072 = 217, taking 3 × (N log2 N )  6.7 × 106 operations.
                 · Roughly a 300× speedup of purely algorithmic origin -- what makes real-time, high-fidelity audio
                    processing possible.

                                                                                                                                                                                                                          14
FFT for Prime Lengths
What if N is Prime? Bluestein's Algorithm

· Cooley­Tukey yields O(N log N ) performance for powers of 2, or for any composite N = N1N2. But what
  if N is a large prime number (e.g., N = 1,000,003)?

· Then N1 = 1, and Cooley­Tukey devolves right back to O(N 2).

· Bluestein's Algorithm brings any DFT length to O(N log N ) by cleverly expressing the DFT as a linear
  convolution -- which we now know how to compute fast.

The Chirp-Z Identity

Start with the algebraic identity for squares:

(k - n)2 = k2 - 2kn + n2                        =            (k - n)2     k2     n2
                                                   kn = -              +      +
                                                   2                   22

Using this, we can substitute kn in the twiddle factor WNkn = W22Nkn giving:

                      WNkn = W2-N(k-n)2 W2kN2 W2nN2

                                                                                                         15
Bluestein's Algorithm: Derivation

· Applying the Chirp-Z Identity to the DFT definition:

                                           N -1

                                   X[k] =        x[n]WNkn

                                           n=0

                                       N -1             W2-N(k-n)2 W2kN2 W2nN2

                                   = x[n]

                                           n=0

                                                 N -1   x[n]W2nN2  W2-N(k-n)2

                                   = W2kN2                   a[n]      b[k-n]

                                                  n=0

· The summation is precisely a linear convolution evaluated at index k!
                                                          X[k] = W2kN2 · (a  b)[k]

  where a[n] = x[n]W2nN2 for n  [0, N - 1] and the chirp filter b[n] = W2-Nn2 for n  [-(N - 1), N - 1].
· We can evaluate this convolution using fast convolution!
· But in this case we need to handle the padding of b[n] with care, as n can be negative.

                                                                                                         16
Visualizing Zero-Padding for Bluestein's Algorithm

a[n]: Padded Data Sequence (N = 16, Pad M = 64)                   M = 64
             x[n]W2nN2
                                                    Zero Pad

                        15         Zero Pad void                                      63

b[n]: Wrapped & Zero-Padded Chirp                                                                n
       Positive n: W2-Nn2
                                                              Wrapped negative n: b[((n))M ]

                                                                          n

15                                                            49  63

· Linear convolution evaluates b[k - n] for n = 0, . . . , N - 1, so the index k - n runs from k - (N - 1) to k:
  it can be negative.

· In a length-M circular buffer a negative index n lands at ((n))M = M + n -- Lecture 2's wrap, now used
  on purpose.

· So the positive indices of b[n] go at the start of the size-M array, the negative indices at the end, and
  zeros in between so the two never overlap: M  2N - 1.

                                                                                                                  17
Bluestein's Fast Convolution

           · How does turning a multiplication into a convolution help?
           · Because we can compute a linear convolution with fast convolution: zero-pad, FFT, multiply, IFFT.
           · Sequence a[n] has length N . Sequence b[n] is needed for n  -(N - 1) . . . (N - 1), so its support length

              is 2N - 1.
           · We can pick any M  2N - 1 and zero-pad both sequences. We intentionally choose M = 2m so we can

              use the highly efficient Radix-2 DIT FFT -- the prime N never touches the transform length.

             Bluestein's FFT Algorithm

                1. Form a[n] = x[n]W2nN2 and the wrapped chirp b[((n))M ], both of size M = 2log2(2N-1).
                2. Compute A = FFT(a, M ) and B = FFT(b, M ) using Radix-2.
                3. Compute Y [k] = A[k]B[k].
                4. Compute y[n] = IFFT(Y, M ).
                5. Multiply by W2kN2 : X[k] = y[k]W2kN2 for k = 0 . . . N - 1.

                                                                                                                                                                                                                          18
The Big Picture
Summary

FFT for any composite N = N1N2                                     Fast convolution
                                                                   Pad to N  L+M -1  FFT both  multiply 
    · Load x[n] column-major into N1 × N2;                         IFFT. O(N log N ) against O(LM ): about 300×
      DFT the rows; twiddle by WNn1k2 ; DFT the                    for one second of audio.
      columns; read row-major.
                                                                   Today in one sentence
    · Radix-2 and Radix-3 are the N1 = 2, 3                        Every N has an O(N log N ) transform -- factor
      cases. Recurse on the factors:                               it if you can, chirp it if you cannot -- and with it,
      O(N log N ) whenever the prime factors                       the fastest known way to filter.
      are small.
                                                                                                                                                               19
FFT for prime N : Bluestein

kn       =  1  (k2  +  n2  -  (k  -  n)2 )  turns  the  DFT  into
            2
a linear convolution with the chirp W2-Nn2 ; run it as
a padded fast convolution of any convenient length

M  2N - 1.


# Ashraf Sir/Lecture 5 - Sampling.pdf

Sampling

Signals and Linear Systems

Ashrafur Rahman
Lecturer, CSE, BUET

ashrafur@cse.buet.ac.bd
Outline

           · Introduction: representing a continuous-time signal by its samples -- and the ambiguity
           · Sampling as multiplication: the time-domain row of the map
           · Two roads to Xp(j): multiply-then-transform (a dead end) versus transform-then-convolve
           · The tools: duality, multiplication  convolution, the spectrum of an impulse train
           · The key observation: convolving with impulses copies the spectrum
           · The Sampling Theorem: Nyquist rate and aliasing
           · Signal Reconstruction: ideal low-pass filtering, zero-order hold, linear interpolation
           · Revisiting the DFT: practical considerations and periodic signals

                                                                                                                                                                                                                            1
Introduction and Terminology
Recap: Representation by Samples

           · In Lecture 1 we turned a continuous-time signal x(t) into a sequence by reading it at uniform intervals,
              x[n] = x(nT ), and never looked back.

           · Question: under what conditions is x(t) uniquely determined by -- and exactly recoverable from -- its
              samples?

           · Exact recovery is possible if the signal is band-limited (its Fourier transform is zero outside a finite band
              of frequencies) and the samples are taken sufficiently close together.

           · This is the Nyquist­Shannon Sampling Theorem. Today we derive it, and the derivation is one picture.

                                                                                                                                                                                                                           2
Ambiguity in Representation by Samples

· Generally, infinitely many continuous-time signals can yield the exactly same discrete sequence when
  sampled at interval T .

x1 (t)  x2 (t)  x3 (t)

                                                       t

-3T     -2T                             -T  T  2T  3T

                                                                                                        3
Sampling as Multiplication: The Time-Domain Row

· To analyze sampling mathematically, represent it as multiplying x(t) by a periodic impulse train p(t).
  (Lecture 1 wrote the period as Ts; here it is simply T .)

                        x(t)                                 p(t)                       xp (t)

                              ×                                    =

                                                          T

Impulse-Train Sampling

        +                                                    +

p(t) =                  (t - nT ),  xp(t) = x(t) p(t) =               x(nT ) (t - nT )

        n=-                                                  n=-

· Each impulse picks up the value of x(t) where it stands, so the weights x(nT ) are exactly the samples
  x[n]. So far, this is the picture from Lecture 1.

                                                                                                                                                                                                            4
Two Roads to Xp(j)
The Map: What We Know and What We Want

· Suppose we know x(t) -- and therefore its spectrum X(j). Sampling hands us xp(t). What is its
  spectrum Xp(j), and how is it related to X(j)?

       x(t)                                      p(t)         xp (t)

             ×                                         =

                                        T

    F                                      F               F

          X (j )                                 P (j)                Xp (j  )

                                              ?         =     ?

-M     M

· Top row: known. Bottom row: two question marks. From the top-left corner to the bottom-right one there
  are two roads.

                                                                                                          5
Road 1: Multiply First, Then Transform

                                        x(t)                                       p(t)              xp (t)

                                              ×                                          =

                                                                          T

                          F                                                  F                 F Road 1

                             X (j )                                                P (j)             Xp (j  )

                                                                                ?         =       ?

-M                           M

The product is already in hand, so just transform it; the impulses sift the integral:

                                                                                             

Xp(j) =                                 x(nT ) (t - nT ) e-jt dt =                                x(nT ) e-jnT

                             - n                                                             n=-

A formula, not a picture

 Correct -- Lecture 1 relabelled T   and called it the DTFT.  It says what Xp(j) is, not how it
looks.  X(j), the one thing we were given, appears nowhere. It cannot be interpreted. Park it.

                                                                                                                6
Road 2: Transform First, Then Convolve

                                   x(t)                                           p(t)         xp (t)

                                         ×                                              =

                                                                     T

                             F                                          F Road 2           F

                                X (j )                                     P (j)                      Xp (j  )

                                                                        ?         =           ?

   -M                           M

· Go down first: X(j) we have, P (j) we can look for. Then combine along the bottom row.

·  A product in time should become a convolution in frequency, Xp(j) =                      1  X(j)  P (j). If so, Xp(j)
                                                                                           2
   is built out of X(j) -- and then maybe, just maybe, we can read off how the two spectra are related.

   Two tools to build first

   (1) Multiplication  convolution, which we get from the convolution property by duality.
   (2) The spectrum P (j) of the impulse train.

                                                                                                                          7
Tool 1: Fourier Transform Duality

· We derive the duality principle from the inverse Fourier transform:
                                        
           1
x(t) =                                  X(j)ejtd = 2x(-t) = X(j)e-jtd
                                   2

· Swapping the names t and :
                                                              

                                             2x(-) = X(jt)e-jtdt = F {X(jt)}

· Hence, the duality principle:

                                             x(t) F X(j) = X(jt) F 2x(-)

· Every transform pair we know comes with a free twin: swap the roles of time and frequency, flip, and
  scale by 2.

                                                                                                        8
Tool 2: Multiplication Is Convolution in the Frequency Domain

· We know from the Convolution Property that,

                        x1(t)  x2(t) F X1(j)X2(j)

· By duality,

                        X1(jt)  X2(jt) F 2x1(-)x2(-)

                        X1(jt) F 2x1(-)

                        X2(jt) F 2x2(-)

· Substituting X1(jt) with u(t) and X2(jt) with v(t):

                        u(t) F 2x1(-) = U (j)

                        v(t) F 2x2(-) = V (j)

· Substituting we get:

                        u(t)v(t) F                     1
                                                          U (j)  V (j)
                                               2

· Hence the bottom row of the map really is a convolution -- one unknown left, P (j):

                                        1
                        Xp(j) = 2 [X(j)  P (j)]

                                                                                       9
Tool 3, First Attempt: P (j) Straight from the Definition

· Transform the train term by term; each impulse sifts:

                                                              p(t)

P (j) =         (t - nT ) e-jt dt =       e-jnT

         - n                         n=-

· The same kind of answer as Road 1, with the same problem:                                                  t
  an infinite sum of complex exponentials in . What does it         T
  look like? Worse, we would have to convolve X(j) with it. 
  Dead end #2.                                                             F

Change of plan                                                                          ?
                                                                           e-jnT

p(t) is periodic with period T , and periodic signals have a        n=-
second representation: the Fourier series. Rewrite p(t) as
a Fourier series first, then transform. Be patient -- in two         true, but what
slides it will be clear why this helps.                             does it look like?

                                                                                                                10
Tool 3, Second Attempt: Fourier Series First

· p(t) has period T , so with s = 2/T :

           +  ck ejkst,               1   T /2                          p(t)
                                      T           p(t) e-jkst dt
p(t) =                     ck      =                                                                                        t
                                           -T /2                                       T
        k=-
                                                                                      Fourier
· Only one impulse, (t), lives inside one period. Sifting:                              series

ck  =   1   T /2                   =  1  e0   =  1  for every k          ck -- every harmonic, equal weight
        T           (t) e-jkst dt     T          T                1
                                                                  T
             -T /2
                                                                                                                            k
The impulse train as a Fourier series                                                       -1 0 1

                        1  +
              p(t) =              ej ks t
              T
                           k=-

· A sum of exponentials again -- but a very different one. Before: e-jnT , functions of  we could not
  draw. Now: ejkst, pure tones in t at the frequencies ks. And the CTFT of a pure tone is the one
  spectrum everybody can draw.

                                                                                                                                                                                                           11
The CTFT of a Pure Tone Is an Impulse

· Sifting gives (t)  1. Duality with x = , X = 1:             p(t)
                         1 F 2 (-) = 2 ()
                                                                    T               t
· Frequency shift, straight from the definition:
       ej0tx(t) F x(t) e-j(-0)t dt = X(j( - 0))               P (j)    F  2
                                                                          T
· Hence a pure tone is a single impulse,
  ejkst  2 ( - ks), and the Fourier series transforms                               
  term by term:

                                                                       s

Spectrum of the impulse train

                                       1  2 +                 ( - ks)
P (j) =                                   2 ( - ks) = T
             T                         k                 k=-

· Good news. An impulse train in time is an impulse train in frequency, spaced s = 2/T apart (closer
  samples, sparser spectrum) -- and impulses are the easiest thing in the world to convolve with.

                                                                                                                                                                                                           12
Why Impulses Are Good News: What Convolution Does

· Recall where convolution came from: an LTI system    (t - t0)    h(t)     h(t - t0)
  with impulse response h(t). Feed it (t), get h(t).
  Feed it (t - t0), get h(t - t0) -- time invariance.  Convolving with impulses just places copies

· Output = input  impulse response, so                                   =

                    (t - t0)  h(t) = h(t - t0)                     0

· Convolving with a shifted impulse does nothing but
  copy h to t0, scaled by the impulse's weight. By
  linearity, convolving with a train of impulses puts
  one copy at every impulse.

· The same in frequency, by sifting:
     X(j)  ( - 0) = X(j) ( -  - 0) d

                                = X(j( - 0))

                                                                                                    13
Back to the Map: Every Impulse Becomes a Copy of X(j)

                                x(t)                                               p(t)          xp (t)

                                      ×                                                  =

                                                                  T

                       F                                             F Road 2                 F

                             X (j )                                             2/T P (j)        1/T Xp(j)

                                                                                           =

            -M               M                                                                s
                                                                             s

Xp(j) =  1          2                  1                                                         1 +
             X(j)            ( - ks) = T                                           X(j)  ( - ks) = T        X j( - ks)
         2          T
                          k                                                     k                     k=-

Spectrum of the sampled signal

Copies of X(j), one at every impulse of P (j): spaced s apart, each scaled by 1/T . This is the

observation behind the Nyquist­Shannon theorem. The copies sit s apart and each is 2M wide --
do they overlap?

                                                                                                                        14
The Sampling Theorem
From the Map to the Theorem

           · Suppose x(t) is band-limited: X(j) = 0 for || > M .
           · On the map, Xp(j) is a row of copies of X(j) centred at 0, ±s, ±2s, . . . ; the copy at ks occupies

              [ks - M , ks + M ].
           · Neighbouring copies stay apart exactly when the right edge of one, M , comes before the left edge of the

              next, s - M :
                                                               M < s - M  s > 2M

           · If they stay apart, the copy at the origin is an untouched X(j)/T , and a low-pass filter can cut it out:
              x(t) is recoverable from its samples.

           · If they overlap, the copies add where they meet, and no filter can un-mix them.

                                                                                                                                                                                                                          15
Nyquist-Shannon Sampling Theorem

             Nyquist-Shannon Sampling Theorem

             Let x(t) be a band-limited signal with X(j) = 0 for || > M . Then x(t) is uniquely determined by
             its samples x(nT ), n = 0, ±1, ±2, . . . , if

                                                                           s > 2M
             where s = 2/T . The minimum sampling frequency 2M is called the Nyquist rate.

    Xp(j)

1/T
                s > 2M

-M                                                       
           M s - M s s + M

                                                                                                               16
Visualizing the Spectrum: Oversampling

                                            X (j )
                                             1

                                                    M                 

                                        -M

                                            Xp(j)

                                        1/T
                                                          Guard band

                                        -M                                                    
                                                    M s - M s s + M

· When s > 2M , exact copies of the original spectrum are perfectly separated.
· The original signal can be recovered by isolating the baseband copy using a low-pass filter!

                                                                                                                                                                                                           17
Visualizing the Spectrum: Undersampling (Aliasing)

        Xp(j)

-s            1/T                                                       s
                                                    Aliasing!
    Aliasing!

                                                    M                      

    -M

· When s < 2M , the shifted copies overlap with the baseband spectrum.

· High frequencies fold over into the low-frequency band, distorting the signal. This phenomenon is called
  aliasing.

· The original signal x(t) cannot be recovered by low-pass filtering.

                                                                                                            18
Signal Reconstruction
Ideal Reconstruction

· By the sampling theorem, if s > 2M , the baseband spectrum of xp(t) (the copy of the spectrum X(j)
  at the origin) is an exact replica of X(j) scaled by 1/T .

· We can recover x(t) by applying an ideal low-pass filter to xp(t).

                      xp(t)  Ideal LPF H(j)                         xr(t) = x(t)

· The frequency response of the ideal LPF must be:           where  M < c < s - M
                                                 {

                                   H(j) = T || < c
                                                   0 || > c

· Commonly, we choose the cutoff frequency exactly in the middle: c = s/2, because it follows the
  assumption that M < s/2.

                                                                                                      19
The Ideal Low-Pass Filter                                   h(t)
                               H (j )                      1
                                T

                                                                                  t
                                       /T
-/T                                                        -3T -T  T  3T

Frequency Response H(j)                                    Impulse Response h(t)

· The frequency response H(j) is a rectangular pulse with cutoff c = s/2 = 2fs/2 = /T .

· The time-domain impulse response h(t) = sinc(t/T ) extends infinitely in both directions, making the
  ideal LPF unrealizable.

                                                                                                        20
Deriving the Ideal Interpolation Filter h(t)

To find the time-domain impulse response h(t) of an ideal low-pass filter with cutoff c = /T
and constant amplitude T , we compute the Inverse Fourier Transform:

h(t) = 1                                               1  /T

             H(j)ejtd =                                        T ejtd
   2 -                                                 2 -/T

=  T ejt /T                                   =  T     ej(/T )t - e-j(/T )t
                                                                  2j
   2 jt -/T t

= T sin t = sinc t                                        Recall sinc(x) = sin(x)
   t      T                                         T                               x

Result: The time-domain filter corresponding to a perfect frequency cutoff is exactly the infinitely
wide sinc function!

                                                                                                      21
Interpolation with the Ideal LPF

· The impulse response h(t) of the ideal LPF (cutoff

c = /T ) is:

                     ()
                     t               sin(t/T )
h(t) = sinc                       =
                     T               t/T

· The reconstructed signal xr(t) = xp(t)  h(t) becomes:                                        t

                +                                                                                        22

xr(t) =              x(nT )(t - nT )  h(t)

                n=-

              +                   (         )
                   x(nT )sinc t - nT
=                                    T

              n=-

· Superposition of shifted sinc functions.

· However, h(t) is non-causal and decays very slowly. It is unrealizable in practice. We need
  approximations.
Zero-Order Hold (ZOH)

The simplest practical reconstruction method is the Zero-Order Hold (ZOH).

                                                   x^(t)

· Concept: Simply hold the sample value
  constant until the next sample arrives.

· This forms a "staircase" approximation x0(t) of
  the continuous signal.

· Widely used in Digital-to-Analog Converters                               t

(DACs).

                                                          T

· We can view this mathematically as filtering the impulse-sampled signal xp(t) with a rectangular pulse
  h0(t).

                                                                                                          23
Why is h0(t) a Rectangle?

· In a reconstructed output signal, an original sample y(nT ) contributes strictly via a shifted, scaled
  version of the base filter: y(nT ) · h(t - nT ).

· The shape of h(t) dictates the weighting of the sample y(nT ) over continuous time.

For Zero-Order Hold:                                           y(nT )
                                                                    1
    · We desire the sample y(nT ) to simply hold its full
      weight of 1 constant precisely until the next sample at                   Weight of y(nT )
      (n + 1)T arrives.                                                              held at 1

    · Thus, the isolated weight of y(nT ) must jump to 1 at    nT  (n + 1)T
      t = nT and abruptly drop back to 0 at t = (n + 1)T .

    · Therefore, the underlying impulse response h0(t) must
      inherently be a rectangular block formally spanning
      from 0 to T !

                                                                                                          24
Deriving the ZOH Frequency Response

The ZOH impulse response h0(t) is simply a rectangular pulse equal to 1 over [0, T ].
We construct H0(j) strictly via continuous Fourier integration:

              h0(t)e-jtdt

H0(j) =                                                h0(t)
                                                       1
         -

=           T              e-jt T

             (1)e-jtdt =    -j 0

         0

= 1 - e-jT          e-jT /2          ejT /2 - e-jT /2
                 =
            j                        j
                                                                                       t
= e-jT /2      2          T                                   T
                 sin                                                                                25
                           2

= T e-jT/2 sinc T
                         2
Frequency Domain view of ZOH                   h0(t)
                              |H0(j)|          1
                                T

                                                                                               t

-s               -  s   s s                           T                                2T  3T
                     2   2

Frequency Response |H0(j)|                     Impulse Response h0(t)

· h0(t) is a rectangle of wid(th T .)Its frequency response includes a sinc function:
H0(j) = T e-jT /2sinc                  T  .
                                       2

We notice that,

· In the passband ||  s/2, the gain is not constant, attenuating high frequencies slightly.
· Outside the passband, the gain is non-zero, allowing high-frequency aliasing copies to leak through.

                                                                                                        26
Linear Interpolation (First-Order Hold)

                                                  x^(t)

· Linear Interpolation connects adjacent samples                                           t
  with straight lines.
                                                                                                         27
· This produces a continuous, much smoother
  approximation x1(t) than the ZOH staircase.

· Achieved by filtering the impulse-sampled
  signal xp(t) with a triangular pulse h1(t).

                                                         T

· The impulse response h1(t) is a triangle spanning [-T, T ] with peak height 1 at t = 0.
Why is h1(t) a Triangle?

· In a reconstructed signal, a given sample y(nT ) contributes via y(nT ) · h1(t - nT ).
· The shape of h1(t) thus dictates the weighting of y(nT ) over time.

For Linear Interpolation:                                                                  y(nT )     Weight
Given a weight   [0, 1], we should have,                                                           falls 1  0 y((n + 1)T )
                                                                                        1
y(t) = (1 - )y((n - 1)T ) + y(nT ) for t  [(n - 1)T, nT ]
                                                                                       Weight
y(t) = (1 - )y(nT ) + y((n + 1)T ) for t  [nT, (n + 1)T ]                          rises 0  1

Therefore,                                                 y((n - 1)T )

    · The weight of y(nT ) should linearly rise strictly   (n - 1)T  nT                            (n + 1)T
      from 0 to 1 between (n - 1)T and nT .

    · It should linearly fall from 1 back to 0 between nT
      and (n + 1)T .

    · At all other times, its weight must precisely be 0
      to isolate its exact local influence.

    · Therefore, h1(t) must inherently be a symmetric
      triangle!

                                                                                                                            28
First-Order Hold: Convolution Intuition

A linear interpolation triangle filter h1(t) can be formed by convolving two shifted zero-order hold

rectangles!                              1
                              h1(t) = T h0(t + T /2)  h0(t + T /2)

Rectangles overlapping                   · h0(t + T /2) is just the standard ZOH block, centered exactly
                                           on time t = 0.

                1   slide                · Area of overlap grows linearly to a peak, and drops cleanly
                                           linearly!

                                         ·  The peak area is T × 1 = T , hence the factor  1  ,  as  the
                                            triangle peak should be 1.                     T

    -        T      T
             2      2
                                         Frequency Derivation: Use F{x  x} = F{x}2.
                                            1                                              2

             h1(t)                          H1(j) = T F h0(t + T /2)
                 1
                                                1                   T sinc T  2
                                            =
                                            T                       2

-T                         T                = T sinc2 T
                                                            2

                                                                                                          29
Frequency Domain view of Linear Interpolation          h1(t)
                              |H1(j)|                  1
                                T

                                                                                                   t

       s   s s                                 -2T -T         T                             2T
        2   2
-s  -

Frequency Response |H1(j)|                     Impulse Response h1(t)

· h1(t) is a triangular pulse spanning [-T, T ]. Its frequency response is H1(j) = T sinc2  ()  .
                                                                                            T
                                                                                            2

· Because of the convolution property, H1(j) is proportional to the square of the ZOH response, without
  the phase delay.

                                                                                                         30
Comparing Reconstruction Filters

           · Let's compare the frequency domain magnitudes against the ideal filter (assuming T = 1):
                                                                   |H (j )|
                                                                                               Ideal

      ZOH

           Linear

                              

-s/2  s/2

· Linear interpolation has much faster high-frequency rolloff (less leakage) than ZOH, making it a "better"
  low-pass filter approximation.

                                                                                                             31
Connection to the DFT
Practical Limitation: Time vs. Frequency            Time-Limited Signal

           The Uncertainty Principle                                                        t

           Signals cannot be both time-limited      -T /2  T /2
           and strictly band-limited!
                                                    Infinite Frequency Spectrum & Aliasing
               · Finite-duration captures mean                        Xp(j)
                  X(j) inherently extends to
                  infinite frequencies.a                   Aliasing Tails                   
                                                                           s
              aInteresting watch: 3Blue1Brown -                                                            32
             Uncertainty Principle

           Unavoidable Aliasing

           Sampling any real-world signal causes
           some aliasing! The infinite spectral
           tails will always overlap and leak into
           our baseband.
DTFT Revisited from the Sampled Signal

Road 1 gave us the CTFT of the sampled impulse train directly:

                                                                    

                                                    Xp(j) =              x[n]e-jnT

                                                                    n=-

                          x[n]e-j (+s )nT                                             |Xp(j)|

   Xp(j( + s)) =                                                                    one period = s

                  n=-

              =   x[n]e-jnT e-j2n

                  n=-

              = Xp(j)

·  Road 2  sT1a ys kthXis(sja(me-fkuncst)i)o.n  is  the  train  of       shifted copy         shifted copy
   copies
                                                                         -s -s/2                              
                                                                                       s/2 s

·  It repeats every s  =  2  .
                          T

· Under T  , the same expression becomes

   the DTFT:

              X(ej) =           x[n]e-j n .

                       n=-

                                                                                                                33
Baseband Copy, Aliasing, and the Ideal LPF

Xp(j) =  1                                            |Xp(j)|
                     X(j( - rs))
         T                                       ideal LPF keeps this band
            r=-                                          original copy

· The central band [-s/2, s/2] contains the
  original copy centered at 0.

· Every other interval of width s is a shifted
  copy of that same spectrum.

· For finite-duration captures the tails are     shifted copy          shifted copy
  infinite, so some aliasing leakage remains,
  but the baseband picture is still the same     -s -s/2                               
  one from the Nyquist proof.                                  s/2 s

· The ideal reconstruction filter keeps exactly

that baseband copy:

            {

H(j) =               T,  || < s/2
                     0,  otherwise

                                                                                         34
Inverse DTFT from the Ideal LPF

· Ideal reconstruction uses one        Applying the mapping at the sample locations,
                                                           
s-wide period of the sampled                            1                     
spectrum:                                                         (ej    )ej  T       T  n
                                       x[n] = x(nT ) =         X                            d
                                                        2
            1   s/2                                  =  1  -
            2            Xp(j)ejt T d                            X(ej )ejn d
x(t)     =                                              2 -
                 -s /2

· After the same mapping T             Inverse DTFT
  used to derive the DTFT,
                                                        
            Xp(j) - X(ej)                         1
                T d - d                x[n] =              X(ej )ejn d
                                                     2 2

· Also,                                As the area is the same regardless of which period we choose.

[-s/2, s/2] T   [-, ]

                                                                                                      35
DFT as Uniform Samples of One s-Wide Period

                                       X[k] = Xp  j ks = X(ej)
                                                  N                2
· Undoing the relabeling, a normalized DTFT                     =  N    k
  point at  sits at the physical frequency
  /T = s/(2).                                        |Xp(j)|

· So an N -point DFT takes N uniformly               DFT evaluates N bins
  spaced samples across one physical
  period of width s.                                                       s/2                     
                                                                                          s
· For even N , bins k = 0, . . . , N/2 run from
  dc to the highest positive frequency.                       positive          wrapped
                                                                                negative
· Bins k = N/2 + 1, . . . , N - 1 then               s /N
  continue as wrapped negative
  frequencies: large negative first, then
  back toward dc.

                                                                                                     36
Periodic Signals Give Harmonic Line Spectra

· If the underlying signal has period T0,         One Period in Time
  then 0 = 2/T0 and

                ak ej k0 t .

x(t) =                                                                               t
                                                                      T0
           k=-                               -T0

· Its CTFT is therefore a line spectrum:

                                                  Harmonic Line Spectrum
                                                          X (j )
X(j) = 2        ak( - k0).

           k=-

· If we sample exactly N times in one
  period, then

T0 = N T,          2
           s = T = N 0.

                                                                             
                                                  0

                                                                                                          37
Sampling Copies the Periodic Line Spectrum

From the Nyquist proof, the sampled spectrum is a  Xp(j)
sum of shifted copies of the original spectrum:
                                                                 possible
         1                                                        overlap
Xp(j) =              X(j( - rs))
         T                                                                                     
            r=-                                                        s

         1                                                                                                                         38

=        T    2      ak(( - rs) - k0)

            r=- k=-

=        2    
                              ak( - k0 - rs)
         T
            r=- k=-

· Each harmonic line is copied to every
  passband.

· Depending on the bandwidth, the copied line
  spectra may overlap and alias into each other.
Nyquist Condition for the Periodic Case

If the original periodic signal is bandlimited to the  Xp(j)
Nyquist band,
                                                              gap: no overlap
                         |k0| < s/2,

then ak = 0 whenever |k|  N/2. The copied line
spectrum becomes

         2   
Xp(j) =                         ak( - k0 - rs).
         T
            r=- |k|<N/2

· Now one passband contains one clean,                                          
  non-overlapping copy of the original                        s
  harmonic line spectrum.
                                                                                                        39
· This is the periodic-signal version of the
  Nyquist condition.
The Same Spectrum from the Sampled Sequence

From Lecture 1 (DTFT and DFT), the sampled periodic                     Xp(j)
signal itself has the Fourier series
                                                                                  same copy locations,
              c ej 0 t ,        1   N-1  x[n]e-j  2  n     1                        now labeled by ck
                                T0                N           X [].
xp(t) =                   c  =                          =
                                                           T0
         =-                         n=0

Since c+N = c, choose any N consecutive indices
K and write  = k + rN :

                                                                                                                         
                                                                                                        s
Xp(j) = 2         c( - 0)

              =-

                

         = 2              ck+rN ( - (k + rN )0)            Coefficient Match

              r=- kK

                                                                        ak ,                            T0
                                                                        T                               T
         = 2              ck( - k0 - rs).                  ck        =        X[k] = T0ck  =                ak  =  N ak

              r=- kK

This equation matches exactly with the previous one.       Hence, if the periodic signal is bandlimited to the Nyquist
Therefore, the coefficients must be related.               band, the DFT bins are scaled versions of the original Fourier
                                                           series coefficients.

                                                                                                                           40
Reconstruction Gives x(t) and the IDFT           Inside one passband only the non-overlapping harmonics remain:
                     T Xp(j)
                                                 x(t) =        1   s/2 T Xp(j)ejt d
                         integrate one passband               2
                                                                   -s /2
                                                                       ck ejk0t =           ak ejk0t.

                                                 =T

                                                              |k|<N/2              |k|<N/2

                                                 So the LPF recovers x(t) exactly when Nyquist holds. With t = nT ,
                                                 T0 = N T :

                                                                                       ck ejk0nT

                                                 x[n] = x(nT ) = T

                                                                              |k|<N/2

-s/2  s/2                                                                  1              [k]ej  2  kn
                                                                       =                         N
                                                                                       X                .
                                                                          N
                                                                              |k|<N/2

                                                 Periodicity of X[k] then shifts the index set to k = 0, . . . , N - 1:

                                                 Inverse DFT

                                                                       1  N-1     [k]ej  2  kn
                                                                                         N
                                                              x[n] =           X
                                                                       N
                                                                          k=0

                                                                                                                         41


# ct3.pdf

Class Test 3                                                                             January 2026

    BANGLADESH UNIVERSITY OF ENGINEERING AND TECHNOLOGY
                     Department of Computer Science and Engineering

                        Course: CSE 219 Signals and Linear Systems

                        Time: 25 minutes                   Marks: 20

Student Name:                                                               Student ID:

Answer all questions. Part A: circle exactly one option. Part B: draw or mark directly on the diagram. No
                                           written explanation is required anywhere.

              Part A -- Multiple choice (1 mark each; circle exactly one option)

1. A real signal is sampled at fs = 8 kHz. Its 8-point DFT magnitude has peaks only at k = 2 and k = 6.

The signal contains:                                                                                   [1]

A. tones at 2 kHz and 6 kHz                         B. a single 2 kHz tone

C. a single 6 kHz tone                              D. tones at 2 kHz and 4 kHz

2. The highest physical frequency any bin of an N -point DFT can represent, for a sampling rate fs, is: [1]
   A. fs B. fs/2 C. (N - 1)fs/N D. N fs

3. The bin spacing f of an N -point DFT is determined by:                                              [1]

A. fs alone B. N alone C. the total recorded duration N Ts D. the amplitude of the signal

4. The DTFT X(ej) of a finite-length sequence is:                                                      [1]

A. a list of N numbers                              B. a continuous, 2-periodic function of 

C. a continuous, aperiodic function of              D. an N -periodic sequence

5. The digital frequency  corresponding to the physical frequency fs/2 is:                             [1]

A. 0 B. /2 C.  D. 2

6. In an N -point DFT, the bin k = N - 1 corresponds to:                                               [1]

A. just below fs (the highest frequency)            B. -fs/N (a small negative frequency)

C. exactly fs/2                                     D. exactly -fs/2

7. The 8-point DFT of x[n] = {1, -1, 1, -1, 1, -1, 1, -1} is nonzero only at:                          [1]

A. k = 0 B. k = 4 C. k = 1 and k = 7 D. k = 2 and k = 6

8. In a 16-point DIT FFT, the sample x[3] appears at input position:                                   [1]

A. 3 B. 6 C. 9 D. 12

9. In a radix-2 DIF butterfly, the multiplication by the twiddle factor happens:                       [1]

A. before the addition/subtraction                  B. after the addition/subtraction

C. only in the final stage                          D. on both inputs

10. A signal sampled at fs = 8 kHz has the 8-point DFT magnitude shown below. Which sequence x[n]

produced it?                                                                                           [1]

                                |X [k]|
                                     8
                                     4

                                          0 1 2 3 4 5 6 7k

A.  x[n] = 1 + cos  2n      B.  x[n] = 1 + cos  4n  C.    x[n] = cos  2n          D. x[n] = 1 + (-1)n
                     8                           8                     8

                    Part B -- Draw / mark on the diagram (2 marks each)

11. The 8-point DFT of a sequence is shown as computed (k = 0, . . . , 7). On the -axis below, redraw the

same spectrum with the negative-frequency bins placed at negative  (principal interval [-, )). Label

each stem with its k.                                                                                  [2]

    |X [k]|

                                                                                         

                 0 1 2 3 4 5 6 7k                          -  -  3    -     -     0       3 
                                                                 4       2     4     4
                                                                                         24
Solution: Stems at  = 0 (k = 0, height 2),  = /4 (k = 1) and  = -/4 (k = 7); nothing at ±.
Bin 7 is the folded negative frequency -2/8.

                                                             k=0

                                                       k=7         k=1

                                                                           

                                        -  -  3  -     -     0           3 
                                              4     2     4        4
                                                                        24

12. A signal sampled at fs = 16 kHz has the 8-point DFT magnitude shown. Fill every box with the physical

frequency (in kHz, with sign) that the bin above it represents.                                  [2]

                            |X [k]|

                                     0 1 2 3 4 5 6 7k

k                           0           1           2           3       4    5             6  7

fk (kHz)

Solution: f = fs/N = 16/8 = 2 kHz; bins above N/2 are (k - N )f . The signal is a 2 kHz tone
(bins 1 and 7 are its ±2 kHz pair).

                                     k        01234 5 6 7

                            fk (kHz) 0 2 4 6 8 -6 -4 -2

13. The periodic sequence x~[n] below has period 4 (one period is {0, 1, 2, 1}). A student takes one period,

zero-pads it to length 8, and computes an 8-point DFT. On the lower axis, draw the periodic sequence

that this 8-point DFT is actually analysing, for n = 0, . . . , 15.                              [2]

x~[n]                                                              2
   2                                                               1
   1
                                                                       0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 n
       0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 n

Solution: The DFT treats its 8 inputs as one period: {0, 1, 2, 1, 0, 0, 0, 0} repeated. The period has
become 8 and the shape has changed, so the bins no longer correspond to the harmonics of the original
period-4 signal.

                               2
                               1

                                   0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 n

14. The 4-point radix-2 DIT FFT below contains two labelling errors. Cross out each wrong label and write

the correct one beside it.                                                                       [2]

                               x[0]                                                 X [0]
                                                                                    X [1]
                               x[1] W20          -1                                 X [2]

                               x[2]                          W40        -1

                               x[3] W20                      W42                    X [3]

                                                 -1                     -1

Solution: (1) DIT inputs must be in bit-reversed order: x[0], x[2], x[1], x[3] (the middle two were
swapped). (2) The second stage-2 twiddle is W41, not W42. Corrected diagram:

                               x[0]                                                 X [0]
                                                                                    X [1]
                               x[2] W20          -1                                 X [2]

                               x[1]                          W40        -1

                               x[3] W20                      W41                    X [3]

                                                 -1                     -1

                                                       Page 2
15. Fill in the two blanks in the iterative radix-2 DIF FFT below (input in natural order).  [2]

1 for s = log2(N) down to 1:

2   M = 2^s

3   W_M = exp(-j 2 pi / M)

4   for l = 0 to N-M step M:

5         W=1

6         for k = 0 to M/2 - 1:

7                  a = x[l + k]

8                  b = x[l + k + M/2]

9                  x[l + k]       =a+b

10                 x[l + k + M/2] = ____________

11                 W = W * W_M

12 Finally , ____________ the array x

    Solution: Line 10: x[l + k + M/2] = (a - b) * W -- subtract first, then multiply by the twiddle
    (the DIF butterfly).
    Line 12: Finally, bit-reverse the array x -- DIF takes natural-order input and produces bit-
    reversed output, so the reordering is done at the end.

                                  Bonus (2 extra marks each)

16. (Bonus) The dashed curve is the DTFT magnitude of the 4-point sequence x[n] = {1, 1, 1, 1}, and the

    dots are its 4-point DFT. The sequence is now zero-padded to length 8. On the axis below, draw the

    magnitude of the 8-point DFT, and circle the stems whose values were already present in the 4-point

    DFT.                                                                                     [+2]

    |X (ej  )|                                    |X [k]|

                0                      3  2                   0 1 2 3 4 5 6 7k
                   2
                                       2

    Solution: Zero-padding does not change the DTFT; the 8-point DFT simply samples the same dashed
    curve at  = 2k/8: heights 4, 2.61, 0, 1.08, 0, 1.08, 0, 2.61. The even bins k = 0, 2, 4, 6 reproduce
    the original four values 4, 0, 0, 0 (circled); the odd bins are new samples between them.

                                    |X [k]|

                                  0 1 2 3 4 5 6 7k

17. (Bonus) Thank you for participating in this CT so early in the morning.                  [+2]

                                          Page 3
