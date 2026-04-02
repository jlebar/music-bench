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
    \time 2/4
    \absolute {
      gis'4 b'4 |
      e''8 gis''8 ais''8 cis''8 |
      b'4 eis''4 |
      b'2 |
      f''2
      \bar "|."
    }
  }
}
