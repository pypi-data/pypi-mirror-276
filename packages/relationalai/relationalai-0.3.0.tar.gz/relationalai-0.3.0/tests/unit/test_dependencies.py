
import pytest
from relationalai import dependencies
from relationalai.dependencies import version_range
from relationalai.errors import RAIInvalidVersionError

#
# Dependencies tests
#

def test_compare_dependencies():
    expected = [
        ('std', '24c1872c-de8a-5b12-7648-3d72f007a7a9',  version_range('0.1.0', '0.2.0')),
        ('graphlib', '04cd9c07-16aa-4433-bdd7-adfdfaee317d',  version_range('0.1.0', '0.2.0'))
    ]
    # correct (does not raise exception)
    dependencies._compare_dependencies(
        expected,
        {
            ('std', '24c1872c-de8a-5b12-7648-3d72f007a7a9'): '0.1.0',
            ('graphlib', '04cd9c07-16aa-4433-bdd7-adfdfaee317d'): '0.1.2'
        },
        None
    )

    # missing a library
    with pytest.raises(RAIInvalidVersionError):
        dependencies._compare_dependencies(
            expected,
            {
                ('std', '24c1872c-de8a-5b12-7648-3d72f007a7a9'): '0.1.0'
            },
            None
        )

    # library version is too old
    with pytest.raises(RAIInvalidVersionError):
        dependencies._compare_dependencies(
            expected,
            {
                ('std', '24c1872c-de8a-5b12-7648-3d72f007a7a9'): '0.0.23',
                ('graphlib', '04cd9c07-16aa-4433-bdd7-adfdfaee317d'): '0.1.2'
            },
            None
        )

    # library version is too new
    with pytest.raises(RAIInvalidVersionError):
        dependencies._compare_dependencies(
            expected,
            {
                ('std', '24c1872c-de8a-5b12-7648-3d72f007a7a9'): '0.2.0',
                ('graphlib', '04cd9c07-16aa-4433-bdd7-adfdfaee317d'): '0.1.2'
            },
            None
        )

    # database needs an update because there's no version data and no std version. This is
    # a reflection of old databases, before we started versioning libraries.
    with pytest.raises(RAIInvalidVersionError):
        dependencies._compare_dependencies(expected, {}, None)

    # relationalai library needs an update because there's a version for std but there is
    # nothing in static lock. This is future proofing when we move versions to some other
    # place, and this version of the library is still in the wild
    with pytest.raises(RAIInvalidVersionError):
        dependencies._compare_dependencies(expected, {}, '0.1.0')

    # currently not possible, but for completeness, a case where one library is too low and
    # another one is too high, which gives an "Incompatible" error
    with pytest.raises(RAIInvalidVersionError):
        dependencies._compare_dependencies(
            expected,
            {
                ('std', '24c1872c-de8a-5b12-7648-3d72f007a7a9'): '0.0.1',
                ('graphlib', '04cd9c07-16aa-4433-bdd7-adfdfaee317d'): '2.1.2'
            },
            '0.1.0'
        )

def test_generate_query():
    assert dependencies._generate_query([
        ('std', '24c1872c-de8a-5b12-7648-3d72f007a7a9', 'irrelevant'),
        ('graphlib', '04cd9c07-16aa-4433-bdd7-adfdfaee317d', 'irrelevant')
    ]).strip() == '''
    @no_diagnostics(:UNDEFINED_IDENTIFIER)
    def output[:std]: { std::version }

    @no_diagnostics(:TYPE_MISMATCH)
    def output(:static_lock, name, uuid, version):
        rel(:pkg, :std, :pkg, :project, :static_lock, name, uuid, version) and
        {
            ("std", "24c1872c-de8a-5b12-7648-3d72f007a7a9") ;
            ("graphlib", "04cd9c07-16aa-4433-bdd7-adfdfaee317d")
        }(name, uuid)'''.strip()
