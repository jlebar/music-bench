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
    \time 4/4
    \absolute {
      g'4 a''8 f''8 gis''4 f''4 |
      bes'4 c'4 e''4 ees'8 e''8 |
      ges''4 bes'8 f'8 a'8 dis'8 e''4 |
      a''4 c''4 g''2 |
      g'2 f'4 gis'4 |
      a'4 ais''4 d'8 d'8 a''4
      \bar "|."
    }
  }
}
