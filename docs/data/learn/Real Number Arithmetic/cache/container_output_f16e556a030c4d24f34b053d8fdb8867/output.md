<div style="border:1px solid black;">

`{bm-disable-all}`

 * Adding 273 and 991...
   * Targeting 2 7 [3]  and 9 9 [1] 
     * Using cache for initial add: 3 + 1 = 4
     * Result: [4] , Carryover: None
   * Targeting 2 [7] 3  and 9 [9] 1 
     * Using cache for initial add: 7 + 9 = 16
     * Result: [6] 4 , Carryover: 1
   * Targeting [2] 7 3  and [9] 9 1 
     * Using cache for initial add: 2 + 9 = 11
     * Using recursion for carryover add: 11 + 1 = ...
       * Adding 11 and 1...
         * Targeting 1 [1]  and [1] 
           * Using cache for initial add: 1 + 1 = 2
           * Result: [2] , Carryover: None
         * Targeting [1] 1  and [0] 1 
           * Using cache for initial add: 1 + 0 = 1
           * Result: [1] 2 , Carryover: None
       * Sum: 12
     * Result: [2] 6 4 , Carryover: 1
   * Remaining carryover: [0] 2 7 3   [1]
   * Result: [1] 2 6 4 
 * Sum: 1264
</div>

`{bm-enable-all}`

