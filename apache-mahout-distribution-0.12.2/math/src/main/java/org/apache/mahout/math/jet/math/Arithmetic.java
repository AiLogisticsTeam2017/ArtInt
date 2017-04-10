/**
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements. See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership. The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License. You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied. See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */
/*
Copyright 1999 CERN - European Organization for Nuclear Research.
Permission to use, copy, modify, distribute and sell this software and its documentation for any purpose 
is hereby granted without fee, provided that the above copyright notice appear in all copies and 
that both that copyright notice and this permission notice appear in supporting documentation. 
CERN makes no representations about the suitability of this software for any purpose. 
It is provided "as is" without expressed or implied warranty.
*/
package org.apache.mahout.math.jet.math;

/**
 * Arithmetic functions.
 */
public final class Arithmetic {

  // for method logFactorial(...)
  // log(k!) for k = 0, ..., 29
  private static final double[] LOG_FACTORIAL_TABLE = {
    0.00000000000000000, 0.00000000000000000, 0.69314718055994531,
    1.79175946922805500, 3.17805383034794562, 4.78749174278204599,
    6.57925121201010100, 8.52516136106541430, 10.60460290274525023,
    12.80182748008146961, 15.10441257307551530, 17.50230784587388584,
    19.98721449566188615, 22.55216385312342289, 25.19122118273868150,
    27.89927138384089157, 30.67186010608067280, 33.50507345013688888,
    36.39544520803305358, 39.33988418719949404, 42.33561646075348503,
    45.38013889847690803, 48.47118135183522388, 51.60667556776437357,
    54.78472939811231919, 58.00360522298051994, 61.26170176100200198,
    64.55753862700633106, 67.88974313718153498, 71.25703896716800901
  };

  // k! for k = 0, ..., 20
  private static final long[] FACTORIAL_TABLE = {
    1L,
    1L,
    2L,
    6L,
    24L,
    120L,
    720L,
    5040L,
    40320L,
    362880L,
    3628800L,
    39916800L,
    479001600L,
    6227020800L,
    87178291200L,
    1307674368000L,
    20922789888000L,
    355687428096000L,
    6402373705728000L,
    121645100408832000L,
    2432902008176640000L
  };

  // k! for k = 21, ..., 170
  private static final double[] LARGE_FACTORIAL_TABLE = {
    5.109094217170944E19,
    1.1240007277776077E21,
    2.585201673888498E22,
    6.204484017332394E23,
    1.5511210043330984E25,
    4.032914611266057E26,
    1.0888869450418352E28,
    3.048883446117138E29,
    8.841761993739701E30,
    2.652528598121911E32,
    8.222838654177924E33,
    2.6313083693369355E35,
    8.68331761881189E36,
    2.952327990396041E38,
    1.0333147966386144E40,
    3.719933267899013E41,
    1.3763753091226346E43,
    5.23022617466601E44,
    2.0397882081197447E46,
    8.15915283247898E47,
    3.34525266131638E49,
    1.4050061177528801E51,
    6.041526306337384E52,
    2.6582715747884495E54,
    1.196222208654802E56,
    5.502622159812089E57,
    2.5862324151116827E59,
    1.2413915592536068E61,
    6.082818640342679E62,
    3.0414093201713376E64,
    1.5511187532873816E66,
    8.06581751709439E67,
    4.274883284060024E69,
    2.308436973392413E71,
    1.2696403353658264E73,
    7.109985878048632E74,
    4.052691950487723E76,
    2.350561331282879E78,
    1.386831185456898E80,
    8.32098711274139E81,
    5.075802138772246E83,
    3.146997326038794E85,
    1.9826083154044396E87,
    1.2688693218588414E89,
    8.247650592082472E90,
    5.443449390774432E92,
    3.6471110918188705E94,
    2.48003554243683E96,
    1.7112245242814127E98,
    1.1978571669969892E100,
    8.504785885678624E101,
    6.123445837688612E103,
    4.470115461512686E105,
    3.307885441519387E107,
    2.4809140811395404E109,
    1.8854947016660506E111,
    1.451830920282859E113,
    1.1324281178206295E115,
    8.94618213078298E116,
    7.15694570462638E118,
    5.797126020747369E120,
    4.7536433370128435E122,
    3.94552396972066E124,
    3.314240134565354E126,
    2.8171041143805494E128,
    2.4227095383672744E130,
    2.107757298379527E132,
    1.854826422573984E134,
    1.6507955160908465E136,
    1.4857159644817605E138,
    1.3520015276784033E140,
    1.2438414054641305E142,
    1.156772507081641E144,
    1.0873661566567426E146,
    1.0329978488239061E148,
    9.916779348709491E149,
    9.619275968248216E151,
    9.426890448883248E153,
    9.332621544394415E155,
    9.332621544394418E157,
    9.42594775983836E159,
    9.614466715035125E161,
    9.902900716486178E163,
    1.0299016745145631E166,
    1.0813967582402912E168,
    1.1462805637347086E170,
    1.2265202031961373E172,
    1.324641819451829E174,
    1.4438595832024942E176,
    1.5882455415227423E178,
    1.7629525510902457E180,
    1.974506857221075E182,
    2.2311927486598138E184,
    2.543559733472186E186,
    2.925093693493014E188,
    3.393108684451899E190,
    3.96993716080872E192,
    4.6845258497542896E194,
    5.574585761207606E196,
    6.689502913449135E198,
    8.094298525273444E200,
    9.875044200833601E202,
    1.2146304367025332E205,
    1.506141741511141E207,
    1.882677176888926E209,
    2.3721732428800483E211,
    3.0126600184576624E213,
    3.856204823625808E215,
    4.974504222477287E217,
    6.466855489220473E219,
    8.471580690878813E221,
    1.1182486511960037E224,
    1.4872707060906847E226,
    1.99294274616152E228,
    2.690472707318049E230,
    3.6590428819525483E232,
    5.0128887482749884E234,
    6.917786472619482E236,
    9.615723196941089E238,
    1.3462012475717523E241,
    1.8981437590761713E243,
    2.6953641378881633E245,
    3.8543707171800694E247,
    5.550293832739308E249,
    8.047926057471989E251,
    1.1749972043909107E254,
    1.72724589045464E256,
    2.5563239178728637E258,
    3.8089226376305687E260,
    5.7133839564458575E262,
    8.627209774233244E264,
    1.3113358856834527E267,
    2.0063439050956838E269,
    3.0897696138473515E271,
    4.789142901463393E273,
    7.471062926282892E275,
    1.1729568794264134E278,
    1.8532718694937346E280,
    2.946702272495036E282,
    4.714723635992061E284,
    7.590705053947223E286,
    1.2296942187394494E289,
    2.0044015765453032E291,
    3.287218585534299E293,
    5.423910666131583E295,
    9.003691705778434E297,
    1.5036165148649983E300,
    2.5260757449731988E302,
    4.2690680090047056E304,
    7.257415615308004E306
  };

  private Arithmetic() {
  }

  /**
   * Efficiently returns the binomial coefficient, often also referred to as "n over k" or "n choose k". The binomial
   * coefficient is defined as <ul> <li>k<0<tt>: <tt>0</tt>. <li>k==0 || k==n<tt>: <tt>1</tt>. <li>k==1 || k==n-1<tt>:
   * <tt>n</tt>. <li>else: <tt>(n * n-1 * ... * n-k+1 ) / ( 1 * 2 * ... * k )</tt>. </ul>
   *
   * @return the binomial coefficient.
   */
  public static double binomial(long n, long k) {
    if (k < 0) {
      return 0;
    }
    if (k == 0 || k == n) {
      return 1;
    }
    if (k == 1 || k == n - 1) {
      return n;
    }

    // try quick version and see whether we get numeric overflows.
    // factorial(..) is O(1); requires no loop; only a table lookup.
    if (n > k) {
      int max = FACTORIAL_TABLE.length + LARGE_FACTORIAL_TABLE.length;
      if (n < max) { // if (n! < inf && k! < inf)
        double nFactorial = factorial((int) n);
        double kFactorial = factorial((int) k);
        double nMinusKFactorial = factorial((int) (n - k));
        double nk = nMinusKFactorial * kFactorial;
        if (nk != Double.POSITIVE_INFINITY) { // no numeric overflow?
          // now this is completely safe and accurate
          return nFactorial / nk;
        }
      }
      if (k > n / 2) {
        k = n - k;
      } // quicker
    }

    // binomial(n,k) = (n * n-1 * ... * n-k+1 ) / ( 1 * 2 * ... * k )
    long a = n - k + 1;
    long b = 1;
    double binomial = 1;
    for (long i = k; i-- > 0;) {
      binomial *= (double) a++ / b++;
    }
    return binomial;
  }

  /**
   * Instantly returns the factorial <tt>k!</tt>.
   *
   * @param k must hold <tt>k &gt;= 0</tt>.
   */
  private static double factorial(int k) {
    if (k < 0) {
      throw new IllegalArgumentException();
    }

    int length1 = FACTORIAL_TABLE.length;
    if (k < length1) {
      return FACTORIAL_TABLE[k];
    }

    int length2 = LARGE_FACTORIAL_TABLE.length;
    if (k < length1 + length2) {
      return LARGE_FACTORIAL_TABLE[k - length1];
    } else {
      return Double.POSITIVE_INFINITY;
    }
  }

  /**
   * Returns <tt>log(k!)</tt>. Tries to avoid overflows. For <tt>k<30</tt> simply looks up a table in O(1). For
   * <tt>k>=30</tt> uses stirlings approximation.
   *
   * @param k must hold <tt>k &gt;= 0</tt>.
   */
  public static double logFactorial(int k) {
    if (k >= 30) {

      double r = 1.0 / k;
      double rr = r * r;
      double c7 = -5.95238095238095238e-04;
      double c5 = 7.93650793650793651e-04;
      double c3 = -2.77777777777777778e-03;
      double c1 = 8.33333333333333333e-02;
      double c0 = 9.18938533204672742e-01;
      return (k + 0.5) * Math.log(k) - k + c0 + r * (c1 + rr * (c3 + rr * (c5 + rr * c7)));
    } else {
      return LOG_FACTORIAL_TABLE[k];
    }
  }

}