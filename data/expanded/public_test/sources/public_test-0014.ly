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
    \time 3/4
    \absolute {
      e'8 b'8 b'4 |
      bis'8 c'8 f''4 |
      c'2 g'4 |
      a'8 c'8 a''8 c''8 g'4 |
      ees'4 aes''2 |
      f'4 c'8 gis''8 |
      dis'4 d''4 g''4 |
      f'8 d'8 f'8 g'8 d''4
      \bar "|."
    }
  }
}
