mecs is a Madurese python stemming library that allows you to transform word in the Madurese language (Bahasa Madura) to their basic form (lemma).
This application also presents the affixes of the word (prefix, suffix and nasal).

## Instalation

```bash
pip install mecs
```

## Example Usage

```python
# import package
from mecs import Stem

# Create stemmer
st = Stem.Stemmer()

# stem
term = "romana"
st.stemming(term)

print("lemma : ", st.lemma)
# roma

print("prefix : ", st.prefix)
# None

print("suffix : ", st.suffix)
# na

print("nasal : ", st.nasal)
# None

```

## Demo

Live demo : [Click here!](http://93.188.163.245:8502/)

## References

- Rachman, F. H., Ifada, N., Wahyuni, S., Ramadani, G. D., & Pawitra, A. (2022, November). ModifiedECS (mECS) Algorithm for Madurese-Indonesian Rule-Based Machine Translation. In _Proceedings of The 2022 International Conference of Science and Information Technology in Smart Administration (ICSINTESA)_ (pp. 51-56). IEEE. DOI: [10.1109/ICSINTESA56431.2022.10041470](https://doi.org/10.1109/ICSINTESA56431.2022.10041470)
- Ifada, N., Rachman, F. H., Syauqy, M. W. M. A., Wahyuni, S., & Pawitra, A. (2023). MadureseSet: Madurese-Indonesian Dataset. _Data in Brief, 48,_ 109035. DOI: [10.1016/j.dib.2023.109035](https://doi.org/10.1016/j.dib.2023.109035)
