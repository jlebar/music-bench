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
    \key bes \major
    \time 2/4
    \absolute {
      ees'8 a'8 ais'4 |
      d''4 g''8 d'8 |
      g'4 c''4 |
      d'2 |
      f''4 fes''8 a''8 |
      c''8 g''8 g'4
      \bar "|."
    }
  }
}
