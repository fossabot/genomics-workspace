from django.db import models

class BlastQueryRecord(models.Model):
    task_id = models.CharField(max_length=32, primary_key=True) # ex. 128c8661c25d45b8-9ca7809a09619db9
    enqueue_date = models.DateTimeField(auto_now_add=True)
    dequeue_date = models.DateTimeField(null=True)
    result_date = models.DateTimeField(null=True)
    result_status = models.CharField(max_length=32, default='WAITING') # ex. WAITING, SUCCESS, NO_ASN, ASN_EMPTY, NO_CSV, CSV_EMPTY

    def __unicode__(self):
        return self.task_id

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('blast:retrieve', args=[str(self.task_id)])

    class Meta:
        verbose_name = 'blast result'

class Organism(models.Model):
    display_name = models.CharField(max_length=200, unique=True, help_text='Scientific or common name') # shown to user
    short_name = models.CharField(max_length=20, unique=True, help_text='This is used for file names and variable names in code') # used in code or filenames
    description = models.TextField(blank=True) # optional
    tax_id = models.PositiveIntegerField('NCBI Taxonomy ID', null=True, blank=True, help_text='This is passed into makeblast') # ncbi tax id

    def __unicode__(self):
        return self.display_name

class BlastDbType(models.Model):
    molecule_type = models.CharField(max_length=4, default='nucl', choices=(
        ('nucl', 'Nucleotide'),
        ('prot', 'Protein'))) # makeblastdb -dbtype
    dataset_type = models.CharField(max_length=50) # 

    def __unicode__(self):
        return u'%s - %s' % (self.get_molecule_type_display(), self.dataset_type)

    class Meta:
        verbose_name = 'blast database type'
        unique_together = ('molecule_type', 'dataset_type')

class BlastDb(models.Model):
    organism = models.ForeignKey(Organism) # 
    type = models.ForeignKey(BlastDbType) # 
    description = models.TextField(blank=True) # shown in blast db selection ui
    title = models.CharField(max_length=200, unique=True) # makeblastdb -title
    fasta_file = models.FileField(upload_to='blastdb') # upload file
    is_shown = models.BooleanField(help_text='Display this database in the BLAST submit form') # to temporarily remove from blast db selection ui
    #sequence_count = models.PositiveIntegerField(null=True, blank=True) # number of sequences in this fasta

    def __unicode__(self):
        return self.fasta_file

    class Meta:
        verbose_name = 'blast database'

class Sequence(models.Model):
    key = models.AutoField(primary_key=True)
    blast_db = models.ForeignKey(BlastDb) # 
    id = models.CharField(max_length=100) # 
    header = models.CharField(max_length=400) # 
    length = models.PositiveIntegerField() # 
    sequence = models.TextField() # 

    def __unicode__(self):
        return self.id

    class Meta:
        unique_together = ('blast_db', 'id')

class JbrowseSetting(models.Model):
    'Used to link databases to Jbrowse'
    blast_db = models.ForeignKey(BlastDb, verbose_name='reference sequence', unique=True, help_text='The BLAST database used as the reference sequence in Jbrowse') # 
    url = models.URLField('Jbrowse URL', unique=True, help_text='The URL to Jbrowse using this reference')

    def __unicode__(self):
        return self.url
