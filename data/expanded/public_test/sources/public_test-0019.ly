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
    \clef treble
    \key f \major
    \time 3/4
    \absolute {
      c'4 e'2 |
      f'4 bes'8 g''8 |
      ais''4 bis'8 e''8 |
      d'8 bes'8 bes'8 d''8 fes''4
      \bar "|."
    }
  }
}
