"""Independent day-by-day oracle and exhaustive small-domain verification."""
import itertools
import unittest
from src.continuity import Window, audit, intersection, safe_starts, count

def oracle(paths, duration, horizon, switching):
    def available(path, day):
        return all(any(w.start <= day < w.end for w in layer) for layer in path)
    good = []
    for t in range(horizon.start, horizon.end):
        days = range(t,t+duration)
        okay = (all(any(available(p,d) for p in paths) for d in days) if switching
                else any(all(available(p,d) for d in days) for p in paths))
        if okay: good.append(t)
    return good

class Verification(unittest.TestCase):
    def test_exhaustive(self):
        windows = [Window(a,b) for a in range(5) for b in range(a+1,6)]
        checked = 0
        for a,b,c in itertools.product(windows, repeat=3):
            paths = [[[a],[b]], [[c]]]
            for r in (1,2,3,5):
                for switching in (False,True):
                    answer = audit(paths,r,Window(0,6),switching)
                    self.assertEqual(answer['safe_days'],len(oracle(paths,r,Window(0,6),switching)))
                    checked += 1
        self.assertEqual(checked,27000)

    def test_switching_changes_order(self):
        paths = [[[Window(0,100)]],[[Window(90,200)]]]
        self.assertEqual(audit(paths,30,Window(0,200),False)['safe_days'],152)
        self.assertEqual(audit(paths,30,Window(0,200),True)['safe_days'],171)

    def test_empty_and_boundary(self):
        self.assertEqual(intersection([[Window(0,10)],[Window(10,20)]]),[])
        self.assertEqual(count(safe_starts([Window(0,30)],30,Window(0,30))),1)
        self.assertEqual(audit([],30,Window(0,365))['safe_days'],0)
        with self.assertRaises(ValueError): Window(2,2)
        with self.assertRaises(TypeError): Window(0,2.5)
        with self.assertRaises(TypeError): safe_starts([],True,Window(0,10))
        with self.assertRaises(ValueError): safe_starts([],0,Window(0,10))

if __name__ == '__main__': unittest.main()
