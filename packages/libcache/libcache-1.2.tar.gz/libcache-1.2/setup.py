from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    readme = f.read()

setup(
        name="libcache", 
        version="1.2",
        author="kuba201",
        description='Simple cache with TTL',
        long_description=readme,
        long_description_content_type='text/markdown',
        packages=find_packages(),
        url="https://flerken.zapto.org:1115/kuba/libcache",
        install_requires=[],
        project_urls={
            'Source': 'https://flerken.zapto.org:1115/kuba/libcache',
        },
        keywords=['cache','temp','ttl'],
        classifiers= [
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3 :: Only",
            "Development Status :: 5 - Production/Stable",
        ]
)