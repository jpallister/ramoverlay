#include "platformcode.h"
#include "snipmath.h"

int main(void)
{
   double  a1 = 1.0, b1 = -10.5, c1 = 32.0, d1 = -30.0;
   double  a2 = 1.0, b2 = -4.5, c2 = 17.0, d2 = -30.0;
   double  a3 = 1.0, b3 = -3.5, c3 = 22.0, d3 = -31.0;
   double  a4 = 1.0, b4 = -13.7, c4 = 1.0, d4 = -35.0;
   double X;
   int     solutions;
   int i;
   unsigned long l = 0x3fed0169L;
   struct int_sqrt q;
   long n = 0;

   double output[48] = {0};
   double *output_pos = &(output[0]);

   initialise_trigger();
   start_trigger();

   for(n = 0; n < (REPEAT_FACTOR>>7)+1; ++n)
   {
      /* solve some cubic functions */
      /* should get 3 solutions: 2, 6 & 2.5   */
      SolveCubic(a1, b1, c1, d1, &solutions, output);
      /* should get 1 solution: 2.5           */
      SolveCubic(a2, b2, c2, d2, &solutions, output);
      SolveCubic(a3, b3, c3, d3, &solutions, output);
      SolveCubic(a4, b4, c4, d4, &solutions, output);
      /* Now solve some random equations */
      for(a1=1;a1<3;a1++) {
         for(b1=10;b1>8;b1--) {
            for(c1=5;c1<6;c1+=0.5) {
               for(d1=-1;d1>-3;d1--) {
                  SolveCubic(a1, b1, c1, d1, &solutions, output_pos);
                  // output_pos += solutions;
                  // output_count += solutions;
               }
            }
         }
      }
   }

   stop_trigger();


   return 0;
}

/* vim: set ts=3 sw=3 et: */
