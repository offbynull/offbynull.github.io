<div style="border:1px solid black;">

`{bm-disable-all}`

 * Subtracting 100 and 11...
   * Targeting 1 0 [0]  and 1 [1] 
     * Not possible -- attempting to borrow
       * Borrowing from next largest 1 [0] 0 
       * Not possible -- attempting to borrow again
         * Borrowing from next largest [1] 0 0 
         * Completed borrowing [0] [10] 0 
       * Completed borrowing [9] [10] 
     * Using cache for subtraction: 10 - 1 = 9
     * Result: [9] 
   * Targeting [9] 10  and [1] 1 
     * Using cache for subtraction: 9 - 1 = 8
     * Result: [8] 9 
   * Targeting [0] 9 10  and [0] 1 1 
     * Using cache for subtraction: 0 - 0 = 0
     * Result: [0] 8 9 
 * Difference: 89
</div>

`{bm-enable-all}`

