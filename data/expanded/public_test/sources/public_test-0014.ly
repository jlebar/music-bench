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
      e'8 b'8 b'8 a'8 dis''4 |
      bis'8 c'8 f''8 c'8 ees'4 |
      c'4 g'2 |
      ais''4 a''4 c''8 g'8 |
      ees'4 aes''4 fis''8 d'8 |
      fes'8 gis''8 e''4 gis''4 |
      dis'2 d''4 |
      ais'8 f'8 g'4 d''4
      \bar "|."
    }
  }
}
