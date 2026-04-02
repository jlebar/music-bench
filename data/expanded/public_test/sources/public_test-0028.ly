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
      g''8 eis''8 c'8 d''8 f'4 c'4 |
      g''4 f'4 g'4 gis'4 |
      g''2 f''2 |
      ais'4 e''2 b'4 |
      bes'4 f''8 d'8 ees''8 eis'8 des''4
      \bar "|."
    }
  }
}
