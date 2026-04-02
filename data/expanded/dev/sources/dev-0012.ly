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
    \key bes \major
    \time 4/4
    \absolute {
      f,4 bes4 ees,2 |
      bes,4 fes8 c8 fis,8 f,8 ais,4 |
      c'4 c8 c8 f,4 a4 |
      b8 ees,8 f4 ces'4 fis4 |
      ees,4 ees,8 bes,8 a4 d4 |
      ees,4 a,8 a,8 d8 des8 cis4 |
      ais4 f4 f8 a8 g4 |
      g8 a,8 f,4 a,4 g,4
      \bar "|."
    }
  }
}
