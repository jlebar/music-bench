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
    \key c \major
    \time 4/4
    \absolute {
      bis'4 g''8 g'8 g'4 |
      f''4 gis'8 e''8 d'8 g''8 |
      f'4 b'2 g'4 |
      b'4 g'8 f''8 des''4 |
      ges''2 b'2
      \bar "|."
    }
  }
}
