import React from 'react';
import './App.css';
import { Logo } from './Logo';
import ReactDOM from 'react-dom'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faMapMarkerAlt, faEnvelope } from '@fortawesome/free-solid-svg-icons';
import { faGithub } from '@fortawesome/free-brands-svg-icons';


function App() {
  return (
    <div className="App">
      <div className="logo">
        <Logo />
      </div>
      <div className="name">
        Kasra Faghihi
      </div>
      <div className="info">
        <span className="item"><FontAwesomeIcon icon={faGithub} />&nbsp;<a href="https://www.github.com/offbynull">offbynull</a></span>
        <span className="item"><FontAwesomeIcon icon={faEnvelope} />&nbsp;offbynull__at__gmail</span>
        <span className="item"><FontAwesomeIcon icon={faMapMarkerAlt} />&nbsp;Cambridge, MA</span>
      </div>
      <div className="nav">
        <span className="item"><a href="#study_notes">study notes</a></span>
        <span className="item"><a href="#study_queue">study queue</a></span>
      </div>
      <h1 id="study_notes">study notes</h1>
      <div>Personal notes from past and current books / online courses / self-studies.</div>
      <h2>current</h2>
      <ul>
        <li><a href="https://htmlpreview.github.io/?https://github.com/offbynull/learn/blob/master/Bioinformatics/output/output.html">Bioinformatics Algorithms 3rd Edition: An Active Learning Approach</a> (source material: <a href="https://www.bioinformaticsalgorithms.org/">book</a>)</li>
        <li><a href="https://htmlpreview.github.io/?https://github.com/offbynull/learn/blob/master/Math/output/output.html">OpenStax Prealgebra</a> (source material: <a href="https://openstax.org/details/books/prealgebra-2e">book</a>)</li>
      </ul>
      <h2>2018</h2>
      <ul>
        <li><a href="https://github.com/offbynull/learn/blob/master/ANTLR%204.pdf">The Definitive ANTLR 4 Reference</a> (source material: <a href="https://pragprog.com/titles/tpantlr2/the-definitive-antlr-4-reference/">book</a>)</li>
        <li><a href="https://github.com/offbynull/learn/blob/master/Floating%20Point%20Arithmetic.pdf">Numerical Computing with IEEE Floating Point Arithmetic</a> (source material: <a href="https://www.amazon.com/Numerical-Computing-Floating-Point-Arithmetic/dp/0898714826">book</a>)</li>
        <li><a href="https://github.com/offbynull/learn/blob/master/Common%20Workflow%20Language.pdf">Common Workflow Language</a> (no source material)</li>
        <li><a href="https://github.com/offbynull/learn/blob/master/Protocol%20Buffers%203.pdf">Protocol Buffers 3</a> (no source material)</li>
        <li><a href="https://github.com/offbynull/learn/blob/master/Flowtype.pdf">Flowtype</a> (no source material)</li>
        <li><a href="https://github.com/offbynull/learn/blob/master/Nuke%2011%20Rotoscoping.pdf">Your First Day of Rotoscoping in NUKE</a> (source material: <a href="https://www.pluralsight.com/courses/your-first-day-rotoscoping-nuke-1217">course</a>)</li>
        <li><a href="https://github.com/offbynull/learn/blob/master/Nuke%2011%20Tracking.pdf">Your First Day of Tracking in NUKE</a> (source material: <a href="https://www.pluralsight.com/courses/your-first-day-tracking-nuke-1206">course</a>)</li>
        <li><a href="https://github.com/offbynull/learn/blob/master/Nuke%2011%20Channels%20and%20Layers.pdf">NUKE Channel Fundamentals</a> (source material: <a href="https://www.pluralsight.com/courses/nuke-channel-fundamentals">course</a>)</li>
      </ul>
      <h2>2017</h2>
      <ul>
        <li><a href="https://github.com/offbynull/learn/blob/master/CUDA.pdf">Introduction to Parallel Programming CUDA</a> (source material: <a href="https://developer.nvidia.com/udacity-cs344-intro-parallel-programming">course</a>)</li>
        <li><a href="https://github.com/offbynull/learn/blob/master/Nuke%2011.pdf">NUKE Fundamentals</a> (source material: <a href="https://www.pluralsight.com/courses/nuke-fundamentals">course</a>)</li>
        <li><a href="https://github.com/offbynull/learn/blob/master/Houdini%2016.pdf">Introduction to Houdini 15</a> (source material: <a href="https://www.pluralsight.com/courses/introduction-houdini-15-2334">course</a>)</li>
        <li><a href="https://github.com/offbynull/learn/blob/master/Houdini%2016%20Objects%20and%20Collisions.pdf">Introduction to Collision in Houdini</a> (source material: <a href="https://www.pluralsight.com/courses/introduction-collisions-houdini-2006">course</a>)</li>
        <li><a href="https://github.com/offbynull/learn/blob/master/Houdini%2016%20Fluids.pdf">Introduction to Fluid Simulations in Houdini</a> (source material: <a href="https://www.pluralsight.com/courses/introduction-fluid-simulations-houdini-2078">course</a>)</li>
        <li><a href="https://github.com/offbynull/learn/blob/master/Houdini%2016%20Oceans.pdf">Introduction to Dynamic Oceans in Houdini</a> (source material: <a href="https://www.pluralsight.com/courses/intro-dynamic-oceans-houdini-2116">course</a>)</li>
        <li><a href="https://github.com/offbynull/learn/blob/master/Houdini%2016%20Particles.pdf">Introduction to Particles in Houdini</a> (source material: <a href="https://www.pluralsight.com/courses/introduction-particles-houdini-900">course</a>)</li>
        <li><a href="https://github.com/offbynull/learn/blob/master/Houdini%2016%20Hair%20and%20Fur.pdf">Introduction to Hair and Fur in Houdini</a> (source material: <a href="https://www.pluralsight.com/courses/houdini-15-hair-fur-introduction">course</a>)</li>
        <li><a href="https://github.com/offbynull/learn/blob/master/Maya%202015.pdf">Introduction to Maya 2015: Interface and Modeling</a> (source material: <a href="https://www.pluralsight.com/courses/intro-maya-2015-1572">course</a>)</li>
        <li><a href="https://github.com/offbynull/learn/blob/master/Maya%202015%20Materials.pdf">Introduction to Maya 2015: Materials</a> (source material: <a href="https://www.pluralsight.com/courses/intro-maya-2015-1572">course</a>)</li>
        <li><a href="https://github.com/offbynull/learn/blob/master/Maya%202015%20Rigging.pdf">Introduction to Maya 2015: Rigging</a> (source material: <a href="https://www.pluralsight.com/courses/intro-maya-2015-1572">course</a>)</li>
        <li><a href="https://github.com/offbynull/learn/blob/master/Maya%202015%20Animation.pdf">Introduction to Maya 2015: Animation</a> (source material: <a href="https://www.pluralsight.com/courses/intro-maya-2015-1572">course</a>)</li>
        <li><a href="https://github.com/offbynull/learn/blob/master/Maya%202015%20Rendering.pdf">Introduction to Maya 2015: Rendering</a> (source material: <a href="https://www.pluralsight.com/courses/intro-maya-2015-1572">course</a>)</li>
      </ul>
      <h1 id="study_queue">study queue</h1>
      <span>Personal backlog of books / online courses.</span>
      <ul>
        <li>
          <a href="https://greenteapress.com/">Think Series</a>
          <ul>
            <li>Think Stats 2nd Edition</li>
            <li>Think Bayes: Bayesian Statistics in Python</li>
            <li>Think DSP: Digital Signal Processing in Python</li>
            <li>Think Complexity 2nd Edition: Exploring Complexity Science with Python</li>
          </ul>
        </li>
        {/* https://www.globalsecurity.org/military/library/policy/army/doctrine-2015-briefing.pdf */}
        <li><a href="https://armypubs.army.mil/epubs/DR_pubs/DR_a/pdf/web/fm6_22.pdf">US Army Field Manual (FM) 6-22 Leader Development</a></li>
        <li><a href="https://fas.org/irp/doddir/army/adp6_22.pdf">US Army Army Doctrine Publication (ADP) 6-22 Army Leadership and the Profession</a></li>
        <li><a href="https://www.springer.com/gp/book/9783030542559">The Algorithm Design Manual 3rd Edition</a></li>
        <li><a href="https://www.amazon.com/Calculus-Early-Transcendentals-James-Stewart/dp/1285741552">Calculus Early Transcendentals 8th Edition</a></li>
        <li>
          <a href="https://openstax.org/subjects/math">OpenStax Math Series</a>
          <ul>
            <li>OpenStax Elementary Algebra</li>
            <li>OpenStax Intermediate Algebra</li>
            <li>OpenStax College Algebra</li>
            <li>OpenStax Algebra and Trigonometry</li>
            <li>OpenStax Precalculus</li>
            <li>OpenStax Calculus Volume 1</li>
            <li>OpenStax Calculus Volume 2</li>
            <li>OpenStax Calculus Volume 3</li>
            <li>OpenStax Introductory Statistics</li>
            <li>OpenStax Introductory Business Statistics</li>
          </ul>
        </li>
        <li>
          <a href="https://openstax.org/subjects/science">OpenStax Science Series</a>
          <ul>
            <li>OpenStax Biology</li>
            <li>OpenStax Concepts of Biology</li>
            <li>OpenStax Microbiology</li>
            <li>OpenStax Chemistry</li>
            <li>OpenStax College Physics</li>
            <li>OpenStax University Physics Volume 1</li>
            <li>OpenStax University Physics Volume 2</li>
            <li>OpenStax University Physics Volume 3</li>
          </ul>
        </li>
        <li><a href="https://www.manning.com/books/math-for-programmers">Math for Programmers</a></li>
        <li><a href="https://hefferon.net/linearalgebra/">Linear Algebra{/*by Jim Hefferon*/}</a></li>
        <li><a href="http://dmitrysoshnikov.com/courses/parsing-algorithms/">Parsing Algorithms{/*by Dmitry Soshnikov*/}</a></li>
        <li><a href="http://dmitrysoshnikov.com/courses/essentials-of-garbage-collectors/">Garbage Collection Algorithms{/*by Dmitry Soshnikov*/}</a></li>
        <li><a href="https://www.amazon.com/Data-Science-Scratch-Principles-Python/dp/1492041130">Data Science from Scratch 2nd Edition</a></li>
        <li><a href="https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-0002-introduction-to-computational-thinking-and-data-science-fall-2016/">Introduction to Computational Thinking</a></li>
        <li><a href="https://dafriedman97.github.io/mlbook/content/introduction.html">Machine Learning from Scratch: Derivations in Concept and Code</a></li>
      </ul>
    </div>
  );
}

export default App;
