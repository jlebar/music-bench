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
      b'4 g''8 g'8 g'4 b'4 |
      e''8 f''8 a'4 g''8 g''8 d''4 |
      f'4 b'2 g'4 |
      b'8 a'8 e''4 aes'8 des'8 ces'4 |
      g'8 e''8 g''4 a'8 dis'8 e''4
      \bar "|."
    }
  }
}
