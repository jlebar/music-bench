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
    \key g \major
    \time 3/4
    \absolute {
      b'4 d'4 g'8 ais''8 |
      gis''4 fis''4 gis'8 bis'8 |
      g'4 g''8 fis''8 a'4 |
      e''4 ges''8 e'8 a''8 g'8 |
      ees''2 c''4 |
      fis'4 aes''4 d''8 ges'8 |
      c''4 fis''4 c''8 c'8
      \bar "|."
    }
  }
}
