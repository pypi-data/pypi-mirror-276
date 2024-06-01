from setuptools import setup

setup(
    name='xerenity',
    version='0.0.4',
    description='Python package for xerenity',
    url='https://xerenity.vercel.app/login',
    author='Andres Velez',
    author_email='svelez@xerenity.co',
    license='BSD 2-clause',
    packages=['xerenity'],
    install_requires=['supabase>=2.4.4','pandas'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.5',
    ],
)
