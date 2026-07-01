import pytest

from app.backend.functions.paginationFunction import amount_to_go, paginationFunction
from app.backend.functions.clampFunction import clamp

@pytest.fixture
def sample_items():
    """
    Generates a list of 50 items. 
    With 10 items per page, this gives exactly 5 pages total.
    """
    return list(range(1, 51))

num_per_page = 10

class TestPaginationFunction:
    def test_amount_to_go(self):
        """
        Amount to go must be a non negative integer number.
        """
        assert isinstance(amount_to_go, int), f"Amount to go must be an integer, got {type(amount_to_go).__name__}."
        assert amount_to_go >= 0, "Amount to go must be a non negative integer."

    def test_pagination_no_items(self):
        """
        Test an empty list.
        """

        items = []
        page_obj, backward, forward, page_num = paginationFunction(items, page_number=None, num_per_page=num_per_page)
        total_possible_pages = page_obj.paginator.num_pages
        
        assert page_num == 1
        assert page_obj.number == 1
        assert total_possible_pages == 1
        assert list(backward) == []
        assert list(forward) == []

    def test_pagination_default_first_page(self, sample_items):
        """
        Tests that passing no page number defaults to page 1 with correct windows.
        """

        page_obj, backward, forward, page_num = paginationFunction(sample_items, page_number=None, num_per_page=num_per_page)
        total_possible_pages = page_obj.paginator.num_pages
        
        assert page_num == 1
        assert page_obj.number == 1
        # No backward pages on page 1.
        assert list(backward) == []
        # Only should show forward pages, at most the amount to go pages forward.
        # Ex, if page 1, forward list should be [2, 3, 4] if amount to go is 3.
        assert list(forward) == list(range(page_num+1, clamp(page_num+amount_to_go+1, 1, total_possible_pages+1)))

    def test_pagination_middle_page_windows(self, sample_items):
        """
        Tests window generation from a middle page (e.g., page 3).
        """

        page_number = 3
        page_obj, backward, forward, page_num = paginationFunction(sample_items, page_number=page_number, num_per_page=num_per_page)
        total_possible_pages = page_obj.paginator.num_pages
        
        assert page_num == page_obj.number
        # If page 3, backward list should be [1, 2]
        assert list(backward) == list(range(max(page_number-amount_to_go, 1), page_num))
        # If page 3, forward list should be [4, 5]
        assert list(forward) == list(range(page_number+1, min(page_number+amount_to_go+1,total_possible_pages+1)))

    def test_pagination_negative_or_zero_page(self, sample_items):
        """
        Tests that negative or zero page numbers safely clamp back to page 1.
        """
        # Testing 0
        _, _, _, page_num_zero = paginationFunction(sample_items, page_number=0, num_per_page=10)
        assert page_num_zero == 1

        # Testing negative number
        _, _, _, page_num_neg = paginationFunction(sample_items, page_number=-5, num_per_page=10)
        assert page_num_neg == 1

    def test_pagination_out_of_bounds_high_page(self, sample_items):
        """
        Tests that a page number higher than total pages clamps to the last page.
        """
        # Max pages is 5 if 51 items total and num per page is 10. We request page 99.

        page_obj, backward, forward, page_num = paginationFunction(sample_items, page_number=99, num_per_page=num_per_page)
        total_possible_pages = page_obj.paginator.num_pages
        
        assert page_num == total_possible_pages
        assert page_obj.number == total_possible_pages
        # amount to go pages backward from 5
        assert list(backward) == list(range(max(total_possible_pages-amount_to_go, 1), total_possible_pages))
        # No pages forward from the last page
        assert list(forward) == []

    def test_pagination_invalid_string_value(self, sample_items, mocker):
        """
        Tests that an invalid string like 'abc' triggers ValueError handling and defaults to 1.
        """
        # Mock the logger to make sure it tracks the exception safely
        mock_logger = mocker.patch("app.backend.functions.paginationFunction.logger")
        
        page_obj, backward, forward, page_num = paginationFunction(sample_items, page_number="abc", num_per_page=10)
        
        assert page_num == 1
        assert page_obj.number == 1
        assert mock_logger.log.called
        assert "Invalid value gotten for page number" in mock_logger.log.call_args[0][0]