<div style="border:1px solid black;">

`{bm-disable-all}`

 * Multiplying 77 and 87...
   * Targeting 77 and 8 [7] 
     * Appending 0s to multiplicand based on position of multiplier (pos 0): 77 8 [7] 
       * Targeting 7 [7]  and 7
         * Using cache for initial mul: 7 * 7 = 49
         * Result: [9] , Carryover: 4
       * Targeting [7] 7  and 7
         * Using cache for initial mul: 7 * 7 = 49
         * Adding carryover: 49 + 4 = 53
         * Result: [3] 9 , Carryover: 5
       * Remaining carryover: [0] 7 7   [5]
       * Result: [5] 3 9 
   * Targeting 77 and [8] 7 
     * Appending 0s to multiplicand based on position of multiplier (pos 1): 770 [8] 7 
       * Targeting 7 7 [0]  and 8
         * Using cache for initial mul: 0 * 8 = 0
         * Result: [0] , Carryover: None
       * Targeting 7 [7] 0  and 8
         * Using cache for initial mul: 7 * 8 = 56
         * Result: [6] 0 , Carryover: 5
       * Targeting [7] 7 0  and 8
         * Using cache for initial mul: 7 * 8 = 56
         * Adding carryover: 56 + 5 = 61
         * Result: [1] 6 0 , Carryover: 6
       * Remaining carryover: [0] 7 7 0   [6]
       * Result: [6] 1 6 0 
   * Summing intermediate results to get final result...
     * Adding 539 to 0
     * Adding 6160 to 539
 * Product: 6699
</div>

`{bm-enable-all}`

