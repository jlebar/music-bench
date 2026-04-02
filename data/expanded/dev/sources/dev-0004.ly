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
      fes'8 a'8 f''4 a'4 g''4 |
      g'8 b'8 f''8 c'8 d''4 f''4 |
      c''4 d'8 d'8 g'8 a'8 c'4 |
      c'2 gis'2 |
      fes''4 des'2 c''4 |
      cis''4 ges'2 f'4
      \bar "|."
    }
  }
}
