\version "2.24.0"

\paper {
  indent = 0\mm
  line-width = 180\mm
  ragged-right = ##t
}

\layout {
  \context {
    \Score
    \override BarNumber.break-visibility = ##(#t #t #t)
    \override BarNumber.self-alignment-X = #CENTER
  }
}

\score {
  \new Staff {
    \set Score.barNumberVisibility = #all-bar-numbers-visible
    \set Score.currentBarNumber = #1
    \clef bass
    \key f \major
    \time 3/4
    \absolute {
      e,8 g,8 e8 e,8 g,4 |
      c8 e,8 ces'4 bes4 |
      a8 b,8 g4 a4 |
      a,8 a,8 c4 f4 |
      eis,4 fes,8 fis,8 cis4 |
      c4 a,8 ais,8 ais4 |
      g,4 ges,8 f8 c'8 f8
      \bar "|."
    }
  }
}
